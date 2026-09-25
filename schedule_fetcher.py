#!/usr/bin/env python3
"""
schedule_fetcher.py — ESPN Schedule Verification Engine
Bay Area Sports Gazette

Fetches live schedule data from ESPN's public APIs (no auth required) and
verifies / corrects GAMES_DATA entries in build_calendar.py.

Usage:
    python3 schedule_fetcher.py --verify
"""

import json
import logging
import sys
from datetime import date, timedelta, datetime

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s  %(message)s",
)
log = logging.getLogger("schedule_fetcher")

# ---------------------------------------------------------------------------
# ESPN public API endpoints — all free, no key required
# ---------------------------------------------------------------------------
ESPN_ENDPOINTS = {
    "nfl":          "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
    "nhl":          "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard",
    "mls":          "https://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard",
    "nwsl":         "https://site.api.espn.com/apis/site/v2/sports/soccer/usa.nwsl/scoreboard",
    "ncaa_football":"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard",
    "ncaa_soccer_m":"https://site.api.espn.com/apis/site/v2/sports/soccer/mens-college-soccer/scoreboard",
}

# HTTP headers that avoid 403 blocks from ESPN
_HEADERS = {
    "Accept": "application/json",
}

# ---------------------------------------------------------------------------
# Bay Area team keyword lists (used for name-matching)
# ---------------------------------------------------------------------------
BAY_AREA_TEAM_KEYWORDS = {
    # NFL
    "nfl":          ["49ers", "San Francisco 49ers"],
    # NHL
    "nhl":          ["Sharks", "San Jose Sharks"],
    # MLS
    "mls":          ["Earthquakes", "San Jose Earthquakes"],
    # NWSL
    "nwsl":         ["Bay FC"],
    # College football
    "ncaa_football":["California Golden Bears", "San José State", "San Jose State",
                     "Stanford Cardinal"],
    # Men's college soccer
    "ncaa_soccer_m":["Santa Clara", "Stanford", "San Jose State", "California"],
}

# ---------------------------------------------------------------------------
# Cache: {(endpoint_key, date_str) -> list[event_dict]}
# ---------------------------------------------------------------------------
_cache: dict = {}


def _fetch_scoreboard(endpoint_key: str, date_str: str) -> list:
    """
    Fetch ESPN scoreboard for a given endpoint and YYYYMMDD date string.
    Returns list of raw ESPN event dicts, or [] on failure.
    Caches results to avoid duplicate network calls.
    """
    cache_key = (endpoint_key, date_str)
    if cache_key in _cache:
        return _cache[cache_key]

    if not HAS_REQUESTS:
        log.warning("'requests' library not installed — cannot fetch ESPN data.")
        _cache[cache_key] = []
        return []

    url = ESPN_ENDPOINTS.get(endpoint_key)
    if not url:
        log.warning("Unknown endpoint key: %s", endpoint_key)
        _cache[cache_key] = []
        return []

    params = {"dates": date_str, "limit": 200}
    try:
        resp = requests.get(url, headers=_HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        events = resp.json().get("events", [])
        _cache[cache_key] = events
        log.debug("Fetched %d events from %s on %s", len(events), endpoint_key, date_str)
        return events
    except Exception as exc:
        log.warning("ESPN fetch failed (%s, %s): %s", endpoint_key, date_str, exc)
        _cache[cache_key] = []
        return []


def _dates_around(date_str: str, days: int = 2) -> list:
    """Return YYYYMMDD strings for ±days around date_str."""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return [date_str]
    result = []
    for delta in range(-days, days + 1):
        result.append((d + timedelta(days=delta)).strftime("%Y%m%d"))
    return result


def _extract_games(events: list) -> list:
    """
    Normalize ESPN event list into simplified dicts:
    {home_team, away_team, home_score, away_score, venue, date_str, source_url}
    """
    out = []
    for ev in events:
        for comp in ev.get("competitions", []):
            competitors = comp.get("competitors", [])
            home = next((c for c in competitors if c.get("homeAway") == "home"), None)
            away = next((c for c in competitors if c.get("homeAway") == "away"), None)
            if not home or not away:
                continue
            venue_obj = comp.get("venue", {})
            links = ev.get("links", [])
            source_url = links[0].get("href", "") if links else ""
            status_obj = comp.get("status", {}) or ev.get("status", {})
            status_type = status_obj.get("type", {})
            is_completed = bool(status_type.get("completed", False) or status_type.get("name") == "STATUS_FINAL")
            status_detail = status_type.get("shortDetail") or status_type.get("detail") or status_type.get("description") or ""

            out.append({
                "home_team":    home["team"].get("displayName", ""),
                "away_team":    away["team"].get("displayName", ""),
                "home_score":   home.get("score"),
                "away_score":   away.get("score"),
                "venue":        venue_obj.get("fullName", ""),
                "venue_city":   (venue_obj.get("address") or {}).get("city", ""),
                "date_str":     ev.get("date", "")[:10],
                "source_url":   source_url,
                "season_type":  ev.get("season", {}).get("type"),  # 1=pre, 2=regular, 3=post
                "is_completed": is_completed,
                "status_detail": status_detail,
            })
    return out


def _name_match_score(a: str, b: str) -> float:
    """
    Return 0.0–1.0 similarity score between two team name strings.
    Uses word-overlap heuristic.
    """
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())
    common = a_words & b_words
    if not common:
        return 0.0
    union = a_words | b_words
    return len(common) / len(union)


def _best_match(
    game: dict, espn_games: list, threshold: float = 0.3
) -> tuple:
    """
    Find the best-matching ESPN game for a GAMES_DATA entry.
    Returns (espn_game_dict | None, confidence_float).
    """
    listed_home = game.get("home_team", "")
    listed_away = game.get("away_team", "")
    best_score = 0.0
    best_match = None

    for eg in espn_games:
        # Try both home/away orderings (ESPN might list them differently)
        score_a = max(
            _name_match_score(listed_home, eg["home_team"]),
            _name_match_score(listed_home, eg["away_team"]),
        )
        score_b = max(
            _name_match_score(listed_away, eg["home_team"]),
            _name_match_score(listed_away, eg["away_team"]),
        )
        combined = (score_a + score_b) / 2
        if combined > best_score:
            best_score = combined
            best_match = eg

    if best_score < threshold:
        return None, 0.0
    return best_match, min(best_score, 1.0)


def _sport_to_endpoints(game: dict) -> list:
    """Map a GAMES_DATA sport + league to relevant ESPN endpoint keys."""
    sport  = game.get("sport", "").lower()
    league = game.get("league", "").lower()
    level  = game.get("level", "").lower()
    if sport == "football":
        if "nfl" in league or level == "pro":
            return ["nfl"]
        if "college" in level or "ncaa" in league or "fbs" in league:
            return ["ncaa_football"]
    if sport == "hockey":
        return ["nhl"]
    if sport == "soccer":
        if "nwsl" in league:
            return ["nwsl"]
        if "mls" in league:
            return ["mls"]
        if "ncaa" in league or "college" in level:
            return ["ncaa_soccer_m"]
    return []


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def verify_game(game: dict) -> dict:
    """
    Verify a single GAMES_DATA entry against ESPN live data.

    Returns:
    {
        'match_found': bool,
        'confidence':  float 0.0–1.0,
        'corrections': {field: corrected_value, ...},
        'source_url':  str,
        'notes':       str,
    }
    """
    result = {
        "match_found": False,
        "confidence":  0.0,
        "corrections": {},
        "source_url":  "",
        "notes":       "",
    }

    endpoints = _sport_to_endpoints(game)
    if not endpoints:
        result["notes"] = "No ESPN endpoint mapped for this sport/league."
        return result

    game_date = game.get("date", "")
    all_espn_games: list = []
    for date_str in _dates_around(game_date, days=2):
        for ep_key in endpoints:
            events = _fetch_scoreboard(ep_key, date_str)
            all_espn_games.extend(_extract_games(events))

    if not all_espn_games:
        result["notes"] = "No ESPN events fetched (API unavailable or no games in window)."
        return result

    match, confidence = _best_match(game, all_espn_games)
    if match is None:
        result["notes"] = "No matching game found in ESPN data."
        return result

    result["match_found"] = True
    result["confidence"]  = round(confidence, 2)
    result["source_url"]  = match.get("source_url", "")

    # --- Build corrections dict ---
    corrections = {}
    listed_home = game.get("home_team", "")
    listed_away = game.get("away_team", "")
    espn_home   = match.get("home_team", "")
    espn_away   = match.get("away_team", "")

    # Detect home/away swap
    if (_name_match_score(listed_home, espn_away) > _name_match_score(listed_home, espn_home)
            and _name_match_score(listed_away, espn_home) > _name_match_score(listed_away, espn_away)):
        corrections["home_team"] = espn_away
        corrections["away_team"] = espn_home
        corrections["_note_swap"] = "Home/away teams appear reversed vs ESPN data."
    else:
        # Check if away_team name differs significantly
        if _name_match_score(listed_away, espn_away) < 0.5:
            corrections["away_team"] = espn_away
        if _name_match_score(listed_home, espn_home) < 0.5:
            corrections["home_team"] = espn_home

    # Venue mismatch
    listed_venue = game.get("venue", "")
    espn_venue   = match.get("venue", "")
    if espn_venue and listed_venue and _name_match_score(listed_venue, espn_venue) < 0.4:
        corrections["venue"] = espn_venue

    # Score corrections (for final games, or when ESPN indicates match is completed)
    is_espn_completed = match.get("is_completed", False)
    if match.get("home_score") is not None and match.get("away_score") is not None:
        try:
            espn_home_score = int(match.get("home_score"))
            espn_away_score = int(match.get("away_score"))
            if is_espn_completed or game.get("status") == "final":
                corrections["home_score"] = espn_home_score
                corrections["away_score"] = espn_away_score
                if is_espn_completed:
                    corrections["status"] = "final"
                if match.get("status_detail"):
                    corrections["status_detail"] = match.get("status_detail")
        except (TypeError, ValueError):
            pass

    result["corrections"] = corrections
    return result


def verify_all(games_list: list) -> None:
    """
    Iterate all games, verify each against ESPN, print a formatted report.
    """
    RESET   = "\033[0m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    RED     = "\033[31m"
    BOLD    = "\033[1m"
    CYAN    = "\033[36m"

    print()
    print(f"{BOLD}{'='*70}{RESET}")
    print(f"{BOLD}  Bay Area Sports Gazette — ESPN Verification Report{RESET}")
    print(f"{BOLD}{'='*70}{RESET}")
    print()

    verified_count   = 0
    unmatched_count  = 0
    corrections_count = 0

    for game in games_list:
        gid    = game.get("id", "?")
        home   = game.get("home_team", "")
        away   = game.get("away_team", "")
        date_s = game.get("date", "")
        sport  = game.get("sport", "")
        league = game.get("league", "")

        label = f"[{gid}]  {away} @ {home}  ({date_s})  {sport}/{league}"
        print(f"{CYAN}{label}{RESET}")

        v = verify_game(game)

        if not v["match_found"]:
            unmatched_count += 1
            reason = v.get("notes", "No match.")
            print(f"  {YELLOW}⚠  UNVERIFIED — {reason}{RESET}")
        else:
            verified_count += 1
            pct = int(v["confidence"] * 100)
            url = v.get("source_url", "")
            if v["corrections"]:
                corrections_count += 1
                print(f"  {RED}✗  MATCH ({pct}% confidence) — CORRECTIONS NEEDED:{RESET}")
                for field, val in v["corrections"].items():
                    if field.startswith("_note"):
                        print(f"       ⚠  {val}")
                    else:
                        old_val = game.get(field, "<missing>")
                        print(f"       {field}: {old_val!r}  →  {val!r}")
                if url:
                    print(f"       source: {url}")
            else:
                print(f"  {GREEN}✓  VERIFIED ({pct}% confidence)  {url}{RESET}")

        print()

    print(f"{BOLD}{'='*70}{RESET}")
    print(f"  Total games:     {len(games_list)}")
    print(f"  Verified:        {GREEN}{verified_count}{RESET}")
    print(f"  Unmatched:       {YELLOW}{unmatched_count}{RESET}  (sport not in ESPN or no API data)")
    print(f"  Need correction: {RED}{corrections_count}{RESET}")
    print(f"{BOLD}{'='*70}{RESET}")
    print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if "--verify" in sys.argv:
        try:
            from build_calendar import GAMES_DATA
        except ImportError as exc:
            print(f"ERROR: Could not import GAMES_DATA from build_calendar.py: {exc}")
            sys.exit(1)
        verify_all(GAMES_DATA)
    else:
        print("Usage: python3 schedule_fetcher.py --verify")
        print()
        print("This tool verifies GAMES_DATA entries in build_calendar.py")
        print("against ESPN public APIs and reports any corrections needed.")
