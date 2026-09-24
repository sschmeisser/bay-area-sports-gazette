#!/usr/bin/env python3
"""
Bay Area & San Jose Sports Weekly Calendar
Clean Editorial 7-Day Calendar Grid with Mobile Ergonomic UX,
Rolling Scores, and Standalone HTML Generation.
"""

import json
import os
import team_logos
import league_standings

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "games.json")

def load_data():
    """Load games and weeks metadata from data/games.json."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            payload = json.load(f)
            return payload.get("games", []), payload.get("weeks", [])
    return [], []

def save_data(games, weeks):
    """Save games and weeks metadata atomically to data/games.json."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    temp_file = DATA_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump({"weeks": weeks, "games": games}, f, indent=2, ensure_ascii=False)
    os.replace(temp_file, DATA_FILE)

# Module-level variables for backward compatibility
GAMES_DATA, WEEKS_META = load_data()

def reload_data():
    """Refresh module-level data if the JSON file changes."""
    global GAMES_DATA, WEEKS_META
    GAMES_DATA, WEEKS_META = load_data()
    return GAMES_DATA, WEEKS_META

def normalize_games(games):
    normalized = []
    for g in games:
        item = dict(g)
        if "status" not in item:
            item["status"] = "upcoming"
        if item["status"] == "final":
            if "result_summary" not in item:
                item["result_summary"] = "Game concluded."
            if "recap_url" not in item:
                item["recap_url"] = item.get("ticket_url", "")
        # Attach verified team logos and colors
        item["home_logo"] = team_logos.get_team_logo(item.get("home_team", ""))
        item["away_logo"] = team_logos.get_team_logo(item.get("away_team", ""))
        item["home_colors"] = team_logos.get_team_colors(item.get("home_team", ""))
        item["away_colors"] = team_logos.get_team_colors(item.get("away_team", ""))
        # Attach verified league/division standings key
        item["standings_key"] = league_standings.classify_game(item)
        normalized.append(item)
    return normalized

def get_standings_data():
    standings_db = league_standings.get_standings_db()
    st_data = {}
    for k, v in standings_db.items():
        v_copy = dict(v)
        v_copy['rows'] = [dict(r) for r in v['rows']]
        for r in v_copy['rows']:
            r['logo'] = team_logos.get_team_logo(r['team'])
        cross_copy = {}
        for team, cinfo in v.get('cross_division_opponents', {}).items():
            c_copy = dict(cinfo)
            c_copy['logo'] = team_logos.get_team_logo(team)
            cross_copy[team] = c_copy
        v_copy['cross_division_opponents'] = cross_copy
        st_data[k] = v_copy
    return st_data

def generate_html():
    reload_data()
    normalized = normalize_games(GAMES_DATA)
    games_str = json.dumps(normalized)
    weeks_str = json.dumps(WEEKS_META)
    standings_str = json.dumps(get_standings_data())

    tmpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calendar_template.html")
    with open(tmpl_path, "r", encoding="utf-8") as f:
        tmpl = f.read()

    rendered = (tmpl.replace("__GAMES_JSON__", games_str)
                    .replace("__WEEKS_JSON__", weeks_str)
                    .replace("__STANDINGS_JSON__", standings_str))

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sports_calendar.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Generated calendar: {out_path}")

    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    if os.path.islink(index_path):
        os.unlink(index_path)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Synchronized index: {index_path}")

    return out_path

if __name__ == "__main__":
    generate_html()
