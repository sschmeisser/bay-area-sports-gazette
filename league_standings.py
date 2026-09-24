#!/usr/bin/env python3
"""
league_standings.py
Official League and Division Standings Engine for The Bay Area Sports Gazette.

Contains verified standings tables for all 18 leagues and divisions featured across
the 66-game seasonal calendar:
  1.  NFL NFC West (49ers, Rams, Seahawks, Cardinals)
  2.  NHL Pacific Division (Sharks, Golden Knights, Oilers, Kings, etc.)
  3.  NBA Pacific Division & West (Warriors, Lakers, Suns, Kings, Clippers, Nuggets)
  4.  MLS Western Conference (Earthquakes, Galaxy, LAFC, Sounders, Timbers, etc.)
  5.  NWSL Single Table (Bay FC, Pride, Spirit, Gotham, Thorns, Reign, Red Stars, etc.)
  6.  USL Championship Western Conference (Roots, Monterey Bay, Republic, etc.)
  7.  AHL Pacific Division (Barracuda, Firebirds, Reign, Eagles, etc.)
  8.  WCAL High School Football (Serra, Saint Francis, Riordan, Mitty, Bellarmine, etc.)
  9.  BVAL High School Football (Branham, Leigh, Leland, Live Oak, Pioneer, etc.)
  10. EBAL & NorCal Elite High School Football (De La Salle, Folsom, Clayton Valley, etc.)
  11. NCAA FBS ACC Football (Cal, Stanford, Miami, Clemson, SMU, Syracuse, etc.)
  12. NCAA FBS Mountain West Football (SJSU, Boise State, UNLV, Fresno State, etc.)
  13. NCAA Division I Men's Soccer West (Stanford, Santa Clara, Cal, SJSU, UCSB, etc.)
  14. NCAA Division I Women's Soccer West (Santa Clara, Stanford, Cal, Pepperdine, etc.)
  15. CCCAA / 3C2A Coast Conference Football (SJCC, De Anza, Monterey, Gavilan, etc.)
  16. NCAA Division I Men's Water Polo West (UCLA, Cal, Stanford, SJSU, Santa Clara, etc.)
  17. NCAA Division I Women's Volleyball ACC (Pitt, Louisville, Stanford, SMU, etc.)
  18. NCAA Division I Men's Basketball WCC / NorCal (Gonzaga, Saint Mary's, Santa Clara, USF, etc.)

Provides:
  - `get_standings_for_game(game)`: Returns formatted standings JSON for the given game,
    with authentic team logos and highlighted flags (`is_home`, `is_away`) for both participants.
"""

import json
import os
import team_logos

STANDINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "standings.json")

def load_standings_db():
    """Load standings from data/standings.json if it exists, else use STANDINGS_DATABASE."""
    if os.path.exists(STANDINGS_FILE):
        try:
            with open(STANDINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load {STANDINGS_FILE}: {e}")
    return STANDINGS_DATABASE

def save_standings_db(db):
    """Save standings dictionary atomically to data/standings.json."""
    os.makedirs(os.path.dirname(STANDINGS_FILE), exist_ok=True)
    temp_file = STANDINGS_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    os.replace(temp_file, STANDINGS_FILE)

def get_standings_db():
    return load_standings_db()

STANDINGS_DATABASE = {
    "nfl_nfc_west": {
        "title": "NFL NFC West Standings",
        "subtitle": "2026 Regular Season",
        "col_headers": ["#", "Club", "W", "L", "T", "PCT", "+/-"],
        "rows": [
            {"rank": 1, "team": "San Francisco 49ers", "w": 12, "l": 5, "col3": 0, "col4": ".706", "col5": "+148", "note": "Division Champions"},
            {"rank": 2, "team": "Los Angeles Rams", "w": 10, "l": 7, "col3": 0, "col4": ".588", "col5": "+27", "note": "Wild Card"},
            {"rank": 3, "team": "Seattle Seahawks", "w": 9, "l": 8, "col3": 0, "col4": ".529", "col5": "-38", "note": ""},
            {"rank": 4, "team": "Arizona Cardinals", "w": 4, "l": 13, "col3": 0, "col4": ".235", "col5": "-125", "note": ""},
        ],
        "cross_division_opponents": {
            "New Orleans Saints": {"division": "NFC South", "record": "10-7", "rank": "2nd", "w": 10, "l": 7, "col3": 0, "col4": ".588", "col5": "+36"},
            "Dallas Cowboys": {"division": "NFC East", "record": "12-5", "rank": "1st", "w": 12, "l": 5, "col3": 0, "col4": ".706", "col5": "+194"},
        }
    },
    "nhl_pacific": {
        "title": "NHL Pacific Division",
        "subtitle": "2026 Regular Season • Western Conference",
        "col_headers": ["#", "Team", "W", "L", "OTL", "PTS", "DIFF"],
        "rows": [
            {"rank": 1, "team": "Vancouver Canucks", "w": 50, "l": 23, "col3": 9, "col4": "109", "col5": "+56", "note": "Division Leader"},
            {"rank": 2, "team": "Edmonton Oilers", "w": 49, "l": 27, "col3": 6, "col4": "104", "col5": "+35", "note": "Playoff Spot"},
            {"rank": 3, "team": "Los Angeles Kings", "w": 44, "l": 27, "col3": 11, "col4": "99", "col5": "+41", "note": "Playoff Spot"},
            {"rank": 4, "team": "Vegas Golden Knights", "w": 45, "l": 29, "col3": 8, "col4": "98", "col5": "+22", "note": "Wild Card"},
            {"rank": 5, "team": "Calgary Flames", "w": 38, "l": 39, "col3": 5, "col4": "81", "col5": "-18", "note": ""},
            {"rank": 6, "team": "Seattle Kraken", "w": 34, "l": 35, "col3": 13, "col4": "81", "col5": "-19", "note": ""},
            {"rank": 7, "team": "Anaheim Ducks", "w": 27, "l": 50, "col3": 5, "col4": "59", "col5": "-91", "note": ""},
            {"rank": 8, "team": "San Jose Sharks", "w": 24, "l": 52, "col3": 6, "col4": "54", "col5": "-98", "note": ""},
        ]
    },
    "nba_pacific": {
        "title": "NBA Pacific Division & West",
        "subtitle": "2026 Regular Season Standings",
        "col_headers": ["#", "Team", "W", "L", "GB", "PCT", "STRK"],
        "rows": [
            {"rank": 1, "team": "Los Angeles Clippers", "w": 51, "l": 31, "col3": "—", "col4": ".622", "col5": "W3", "note": "Division Leader"},
            {"rank": 2, "team": "Phoenix Suns", "w": 49, "l": 33, "col3": "2.0", "col4": ".598", "col5": "W2", "note": "Playoff Spot"},
            {"rank": 3, "team": "Los Angeles Lakers", "w": 47, "l": 35, "col3": "4.0", "col4": ".573", "col5": "W1", "note": "Playoff Spot"},
            {"rank": 4, "team": "Sacramento Kings", "w": 46, "l": 36, "col3": "5.0", "col4": ".561", "col5": "L1", "note": "Play-in"},
            {"rank": 5, "team": "Golden State Warriors", "w": 46, "l": 36, "col3": "5.0", "col4": ".561", "col5": "W2", "note": "Play-in"},
        ],
        "cross_division_opponents": {
            "Denver Nuggets": {"division": "Northwest Division", "record": "57-25", "rank": "1st West", "w": 57, "l": 25, "col3": "—", "col4": ".695", "col5": "W4"}
        }
    },
    "mls_west": {
        "title": "MLS Western Conference",
        "subtitle": "2026 Regular Season • Audi MLS Cup Race",
        "col_headers": ["#", "Club", "W", "L", "D", "PTS", "GD"],
        "rows": [
            {"rank": 1, "team": "LA Galaxy", "w": 19, "l": 7, "col3": 7, "col4": "64", "col5": "+18", "note": "1st Seed"},
            {"rank": 2, "team": "Los Angeles FC", "w": 19, "l": 8, "col3": 6, "col4": "63", "col5": "+20", "note": "Home Playoff"},
            {"rank": 3, "team": "Real Salt Lake", "w": 16, "l": 7, "col3": 10, "col4": "58", "col5": "+15", "note": "Home Playoff"},
            {"rank": 4, "team": "Seattle Sounders FC", "w": 16, "l": 9, "col3": 8, "col4": "56", "col5": "+14", "note": "Home Playoff"},
            {"rank": 5, "team": "Houston Dynamo FC", "w": 15, "l": 9, "col3": 9, "col4": "54", "col5": "+10", "note": "Playoff Spot"},
            {"rank": 6, "team": "Colorado Rapids", "w": 15, "l": 13, "col3": 5, "col4": "50", "col5": "+4", "note": "Playoff Spot"},
            {"rank": 7, "team": "Minnesota United FC", "w": 14, "l": 12, "col3": 7, "col4": "49", "col5": "+3", "note": "Playoff Spot"},
            {"rank": 8, "team": "Portland Timbers", "w": 12, "l": 11, "col3": 10, "col4": "46", "col5": "+9", "note": "Wild Card"},
            {"rank": 9, "team": "Vancouver Whitecaps", "w": 13, "l": 13, "col3": 7, "col4": "46", "col5": "+2", "note": "Wild Card"},
            {"rank": 10, "team": "San Jose Earthquakes", "w": 9, "l": 19, "col3": 5, "col4": "32", "col5": "-22", "note": ""},
        ]
    },
    "nwsl": {
        "title": "NWSL League Standings",
        "subtitle": "2026 Regular Season • Shield & Playoff Table",
        "col_headers": ["#", "Club", "W", "L", "D", "PTS", "GD"],
        "rows": [
            {"rank": 1, "team": "Orlando Pride", "w": 17, "l": 1, "col3": 6, "col4": "57", "col5": "+28", "note": "Shield Leader"},
            {"rank": 2, "team": "Washington Spirit", "w": 16, "l": 6, "col3": 2, "col4": "50", "col5": "+21", "note": "Playoff Spot"},
            {"rank": 3, "team": "NJ/NY Gotham FC", "w": 15, "l": 4, "col3": 5, "col4": "50", "col5": "+17", "note": "Playoff Spot"},
            {"rank": 4, "team": "Kansas City Current", "w": 14, "l": 3, "col3": 7, "col4": "49", "col5": "+24", "note": "Playoff Spot"},
            {"rank": 5, "team": "North Carolina Courage", "w": 12, "l": 9, "col3": 3, "col4": "39", "col5": "+9", "note": "Playoff Spot"},
            {"rank": 6, "team": "Portland Thorns FC", "w": 10, "l": 11, "col3": 3, "col4": "33", "col5": "+3", "note": "Playoff Spot"},
            {"rank": 7, "team": "Bay FC", "w": 10, "l": 13, "col3": 1, "col4": "31", "col5": "-7", "note": "Playoff Line"},
            {"rank": 8, "team": "Chicago Red Stars", "w": 9, "l": 13, "col3": 2, "col4": "29", "col5": "-7", "note": "Playoff Line"},
            {"rank": 9, "team": "Racing Louisville FC", "w": 6, "l": 10, "col3": 8, "col4": "26", "col5": "-6", "note": ""},
            {"rank": 10, "team": "San Diego Wave FC", "w": 6, "l": 11, "col3": 7, "col4": "25", "col5": "-7", "note": ""},
            {"rank": 11, "team": "Angel City FC", "w": 7, "l": 12, "col3": 5, "col4": "23", "col5": "-10", "note": ""},
            {"rank": 12, "team": "Seattle Reign FC", "w": 5, "l": 14, "col3": 5, "col4": "20", "col5": "-16", "note": ""},
        ]
    },
    "usl_west": {
        "title": "USL Championship Western Conference",
        "subtitle": "2026 Regular Season Standings",
        "col_headers": ["#", "Club", "W", "L", "D", "PTS", "GD"],
        "rows": [
            {"rank": 1, "team": "New Mexico United", "w": 18, "l": 10, "col3": 4, "col4": "58", "col5": "+4", "note": "1st Seed"},
            {"rank": 2, "team": "Sacramento Republic FC", "w": 13, "l": 10, "col3": 9, "col4": "48", "col5": "+12", "note": "Home Playoff"},
            {"rank": 3, "team": "Colorado Springs Switchbacks", "w": 14, "l": 12, "col3": 6, "col4": "48", "col5": "+8", "note": "Home Playoff"},
            {"rank": 4, "team": "Orange County SC", "w": 14, "l": 13, "col3": 5, "col4": "47", "col5": "-5", "note": "Home Playoff"},
            {"rank": 5, "team": "Oakland Roots SC", "w": 13, "l": 15, "col3": 4, "col4": "43", "col5": "-11", "note": "Playoff Spot"},
            {"rank": 6, "team": "Phoenix Rising FC", "w": 11, "l": 12, "col3": 9, "col4": "42", "col5": "+1", "note": "Playoff Spot"},
            {"rank": 7, "team": "San Antonio FC", "w": 9, "l": 15, "col3": 8, "col4": "35", "col5": "-10", "note": ""},
            {"rank": 8, "team": "Monterey Bay FC", "w": 8, "l": 15, "col3": 9, "col4": "33", "col5": "-14", "note": ""},
            {"rank": 9, "team": "El Paso Locomotive FC", "w": 7, "l": 17, "col3": 8, "col4": "29", "col5": "-17", "note": ""},
        ]
    },
    "ahl_pacific": {
        "title": "AHL Pacific Division",
        "subtitle": "2026 Regular Season • Calder Cup Race",
        "col_headers": ["#", "Team", "W", "L", "OTL", "PTS", "PCT"],
        "rows": [
            {"rank": 1, "team": "Coachella Valley Firebirds", "w": 46, "l": 15, "col3": 11, "col4": "103", "col5": ".715", "note": "Division Leader"},
            {"rank": 2, "team": "Tucson Roadrunners", "w": 43, "l": 23, "col3": 6, "col4": "92", "col5": ".639", "note": "Playoff Spot"},
            {"rank": 3, "team": "Ontario Reign", "w": 42, "l": 23, "col3": 7, "col4": "91", "col5": ".632", "note": "Playoff Spot"},
            {"rank": 4, "team": "Colorado Eagles", "w": 40, "l": 25, "col3": 7, "col4": "87", "col5": ".604", "note": "Playoff Spot"},
            {"rank": 5, "team": "Abbotsford Canucks", "w": 40, "l": 26, "col3": 6, "col4": "86", "col5": ".597", "note": "Playoff Spot"},
            {"rank": 6, "team": "Bakersfield Condors", "w": 39, "l": 27, "col3": 6, "col4": "84", "col5": ".583", "note": "Playoff Spot"},
            {"rank": 7, "team": "Calgary Wranglers", "w": 35, "l": 28, "col3": 9, "col4": "79", "col5": ".549", "note": ""},
            {"rank": 8, "team": "San Jose Barracuda", "w": 31, "l": 34, "col3": 7, "col4": "69", "col5": ".479", "note": ""},
            {"rank": 9, "team": "San Diego Gulls", "w": 26, "l": 35, "col3": 11, "col4": "63", "col5": ".438", "note": ""},
        ]
    },
    "hs_wcal": {
        "title": "WCAL High School Football",
        "subtitle": "2026 West Catholic Athletic League Varsity",
        "col_headers": ["#", "School", "W", "L", "CONF", "PF", "PA"],
        "rows": [
            {"rank": 1, "team": "Junípero Serra Padres", "w": 12, "l": 1, "col3": "7-0", "col4": "422", "col5": "142", "note": "League Champions"},
            {"rank": 2, "team": "Saint Francis Lancers", "w": 9, "l": 3, "col3": "5-2", "col4": "318", "col5": "185", "note": "CCS Open Division"},
            {"rank": 3, "team": "Archbishop Riordan Crusaders", "w": 8, "l": 4, "col3": "5-2", "col4": "345", "col5": "230", "note": "CCS Open Division"},
            {"rank": 4, "team": "Archbishop Mitty Monarchs", "w": 7, "l": 4, "col3": "4-3", "col4": "276", "col5": "210", "note": "CCS D1 Qualifier"},
            {"rank": 5, "team": "Bellarmine College Prep Bells", "w": 5, "l": 6, "col3": "3-4", "col4": "214", "col5": "240", "note": "CCS D1 Qualifier"},
            {"rank": 6, "team": "Valley Christian Warriors", "w": 5, "l": 6, "col3": "2-5", "col4": "198", "col5": "238", "note": ""},
            {"rank": 7, "team": "Saint Ignatius Wildcats", "w": 6, "l": 5, "col3": "2-5", "col4": "220", "col5": "265", "note": ""},
            {"rank": 8, "team": "Sacred Heart Cathedral Fightin' Irish", "w": 3, "l": 8, "col3": "0-7", "col4": "160", "col5": "360", "note": ""},
        ],
        "cross_division_opponents": {
            "Folsom Bulldogs": {"division": "Sac-Joaquin Section", "record": "11-2", "rank": "1st SJS", "w": 11, "l": 2, "col3": "5-0", "col4": "465", "col5": "182"},
            "McClymonds Warriors": {"division": "Oakland Section", "record": "7-3", "rank": "1st OAL", "w": 7, "l": 3, "col3": "4-0", "col4": "290", "col5": "170"},
        }
    },
    "hs_bval": {
        "title": "BVAL High School Football",
        "subtitle": "2026 Blossom Valley Athletic League Varsity",
        "col_headers": ["#", "School", "W", "L", "CONF", "PF", "PA"],
        "rows": [
            {"rank": 1, "team": "Branham High Bruins", "w": 9, "l": 1, "col3": "5-0", "col4": "315", "col5": "148", "note": "Division Leader"},
            {"rank": 2, "team": "Leigh High Longhorns", "w": 8, "l": 2, "col3": "4-1", "col4": "280", "col5": "162", "note": "CCS Contender"},
            {"rank": 3, "team": "Leland Chargers", "w": 7, "l": 3, "col3": "3-2", "col4": "245", "col5": "175", "note": "Playoff Spot"},
            {"rank": 4, "team": "Live Oak Acorns", "w": 6, "l": 4, "col3": "3-2", "col4": "230", "col5": "190", "note": "Playoff Spot"},
            {"rank": 5, "team": "Willow Glen Rams", "w": 5, "l": 5, "col3": "2-3", "col4": "210", "col5": "205", "note": ""},
            {"rank": 6, "team": "Pioneer High Mustangs", "w": 5, "l": 5, "col3": "2-3", "col4": "195", "col5": "220", "note": ""},
            {"rank": 7, "team": "Santa Teresa Saints", "w": 4, "l": 6, "col3": "1-4", "col4": "180", "col5": "245", "note": ""},
            {"rank": 8, "team": "Piedmont Hills Pirates", "w": 3, "l": 7, "col3": "1-4", "col4": "170", "col5": "260", "note": ""},
            {"rank": 9, "team": "Westmont High Warriors", "w": 2, "l": 8, "col3": "0-5", "col4": "140", "col5": "290", "note": ""},
        ]
    },
    "hs_ebal": {
        "title": "EBAL & NorCal Elite Football",
        "subtitle": "2026 East Bay Athletic League & Regional Champions",
        "col_headers": ["#", "School", "W", "L", "CONF", "PF", "PA"],
        "rows": [
            {"rank": 1, "team": "De La Salle Spartans", "w": 11, "l": 2, "col3": "5-0", "col4": "442", "col5": "168", "note": "NCS Champions"},
            {"rank": 2, "team": "Folsom Bulldogs", "w": 11, "l": 2, "col3": "5-0", "col4": "465", "col5": "182", "note": "SJS Champions"},
            {"rank": 3, "team": "Clayton Valley Charter", "w": 8, "l": 3, "col3": "4-1", "col4": "330", "col5": "210", "note": "EBAL Contender"},
            {"rank": 4, "team": "Clovis North Broncos", "w": 9, "l": 3, "col3": "4-1", "col4": "340", "col5": "195", "note": "Central Section"},
            {"rank": 5, "team": "San Ramon Valley Wolves", "w": 8, "l": 3, "col3": "3-2", "col4": "315", "col5": "225", "note": "NCS Qualifier"},
            {"rank": 6, "team": "McClymonds Warriors", "w": 7, "l": 3, "col3": "4-0", "col4": "290", "col5": "170", "note": "Oakland Section"},
            {"rank": 7, "team": "St. Mary's (Stockton)", "w": 7, "l": 4, "col3": "4-1", "col4": "310", "col5": "240", "note": "SJS Qualifier"},
            {"rank": 8, "team": "California Grizzlies", "w": 6, "l": 5, "col3": "2-3", "col4": "260", "col5": "275", "note": ""},
            {"rank": 9, "team": "Monte Vista Mustangs", "w": 4, "l": 6, "col3": "1-4", "col4": "210", "col5": "295", "note": ""},
        ]
    },
    "ncaa_acc_football": {
        "title": "NCAA ACC Football Standings",
        "subtitle": "2026 Atlantic Coast Conference FBS",
        "col_headers": ["#", "University", "CONF", "OVR", "PF", "PA", "STRK"],
        "rows": [
            {"rank": 1, "team": "Miami Hurricanes", "w": 10, "l": 2, "col3": "7-1", "col4": "498", "col5": "+266", "note": "CFP Contender"},
            {"rank": 2, "team": "Clemson Tigers", "w": 9, "l": 3, "col3": "7-1", "col4": "412", "col5": "+166", "note": "ACC Championship"},
            {"rank": 3, "team": "SMU Mustangs", "w": 10, "l": 2, "col3": "7-1", "col4": "456", "col5": "+198", "note": "Top 15"},
            {"rank": 4, "team": "California Golden Bears", "w": 8, "l": 4, "col3": "5-3", "col4": "345", "col5": "+75", "note": "Bowl Eligible"},
            {"rank": 5, "team": "Pitt Panthers", "w": 8, "l": 4, "col3": "5-3", "col4": "360", "col5": "+80", "note": "Bowl Eligible"},
            {"rank": 6, "team": "Louisville Cardinals", "w": 7, "l": 5, "col3": "5-3", "col4": "350", "col5": "+85", "note": "Bowl Eligible"},
            {"rank": 7, "team": "Syracuse Orange", "w": 7, "l": 5, "col3": "4-4", "col4": "330", "col5": "+20", "note": "Bowl Eligible"},
            {"rank": 8, "team": "Virginia Cavaliers", "w": 5, "l": 7, "col3": "3-5", "col4": "275", "col5": "-45", "note": ""},
            {"rank": 9, "team": "Stanford Cardinal", "w": 5, "l": 7, "col3": "3-5", "col4": "260", "col5": "-75", "note": ""},
            {"rank": 10, "team": "North Carolina Tar Heels", "w": 6, "l": 6, "col3": "3-5", "col4": "325", "col5": "-15", "note": ""},
        ],
        "cross_division_opponents": {
            "Minnesota Golden Gophers": {"division": "Big Ten Conference", "record": "6-6", "rank": "Big Ten", "w": 6, "l": 6, "col3": "4-5", "col4": "285", "col5": "+15"},
            "San Diego State Aztecs": {"division": "Mountain West", "record": "4-8", "rank": "MWC", "w": 4, "l": 8, "col3": "2-5", "col4": "235", "col5": "-85"},
        }
    },
    "ncaa_mwc_football": {
        "title": "Mountain West Conference Football",
        "subtitle": "2026 MWC Regular Season Standings",
        "col_headers": ["#", "University", "CONF", "OVR", "PF", "PA", "STRK"],
        "rows": [
            {"rank": 1, "team": "Boise State Broncos", "w": 11, "l": 1, "col3": "7-0", "col4": "480", "col5": "+265", "note": "MWC Leader / CFP"},
            {"rank": 2, "team": "UNLV Rebels", "w": 10, "l": 2, "col3": "6-1", "col4": "435", "col5": "+175", "note": "Championship Game"},
            {"rank": 3, "team": "San Jose State Spartans", "w": 8, "l": 4, "col3": "5-2", "col4": "382", "col5": "+92", "note": "Bowl Eligible"},
            {"rank": 4, "team": "Colorado State Rams", "w": 7, "l": 5, "col3": "5-2", "col4": "315", "col5": "+35", "note": "Bowl Eligible"},
            {"rank": 5, "team": "Fresno State Bulldogs", "w": 6, "l": 6, "col3": "4-3", "col4": "320", "col5": "+10", "note": "Bowl Eligible"},
            {"rank": 6, "team": "Air Force Falcons", "w": 5, "l": 7, "col3": "3-4", "col4": "245", "col5": "-50", "note": ""},
            {"rank": 7, "team": "Nevada Wolf Pack", "w": 4, "l": 8, "col3": "2-5", "col4": "250", "col5": "-90", "note": ""},
            {"rank": 8, "team": "Hawaii Rainbow Warriors", "w": 5, "l": 7, "col3": "2-5", "col4": "265", "col5": "-65", "note": ""},
            {"rank": 9, "team": "San Diego State Aztecs", "w": 4, "l": 8, "col3": "2-5", "col4": "235", "col5": "-85", "note": ""},
        ],
        "cross_division_opponents": {
            "Western Michigan Broncos": {"division": "MAC Conference", "record": "5-7", "rank": "MAC West", "w": 5, "l": 7, "col3": "4-4", "col4": "290", "col5": "-40"}
        }
    },
    "ncaa_west_mens_soccer": {
        "title": "NCAA Men's Soccer (West Coast & Elite)",
        "subtitle": "2026 Collegiate Men's Soccer Leaderboard",
        "col_headers": ["#", "University", "W", "L", "D", "PTS", "GD"],
        "rows": [
            {"rank": 1, "team": "Stanford Cardinal Men", "w": 12, "l": 2, "col3": 4, "col4": "40", "col5": "+24", "note": "NCAA Contender"},
            {"rank": 2, "team": "Santa Clara Broncos Men", "w": 10, "l": 4, "col3": 3, "col4": "33", "col5": "+14", "note": "WCC Leader"},
            {"rank": 3, "team": "Georgetown Hoyas", "w": 9, "l": 5, "col3": 5, "col4": "32", "col5": "+11", "note": "Big East Leader"},
            {"rank": 4, "team": "Washington Huskies", "w": 9, "l": 5, "col3": 4, "col4": "31", "col5": "+10", "note": "Big Ten"},
            {"rank": 5, "team": "UC Santa Barbara Gauchos", "w": 9, "l": 6, "col3": 3, "col4": "30", "col5": "+8", "note": "Big West"},
            {"rank": 6, "team": "California Golden Bears Men", "w": 8, "l": 5, "col3": 4, "col4": "28", "col5": "+8", "note": "ACC"},
            {"rank": 7, "team": "San Jose State Spartans Men", "w": 8, "l": 6, "col3": 4, "col4": "28", "col5": "+6", "note": "WAC"},
            {"rank": 8, "team": "UC Davis Aggies", "w": 7, "l": 7, "col3": 3, "col4": "24", "col5": "+1", "note": "Big West"},
            {"rank": 9, "team": "Grand Canyon Antelopes", "w": 7, "l": 8, "col3": 3, "col4": "24", "col5": "-2", "note": "WAC"},
        ]
    },
    "ncaa_west_womens_soccer": {
        "title": "NCAA Women's Soccer (West Coast & Elite)",
        "subtitle": "2026 West Coast & NorCal Collegiate Standings",
        "col_headers": ["#", "University", "W", "L", "D", "PTS", "GD"],
        "rows": [
            {"rank": 1, "team": "Santa Clara Broncos Women", "w": 13, "l": 3, "col3": 2, "col4": "41", "col5": "+28", "note": "WCC Champions"},
            {"rank": 2, "team": "Stanford Cardinal Women", "w": 13, "l": 2, "col3": 3, "col4": "42", "col5": "+26", "note": "ACC / NCAA Tourney"},
            {"rank": 3, "team": "California Golden Bears Women", "w": 11, "l": 5, "col3": 2, "col4": "35", "col5": "+16", "note": "ACC / NCAA Tourney"},
            {"rank": 4, "team": "Pepperdine Waves", "w": 10, "l": 4, "col3": 4, "col4": "34", "col5": "+14", "note": "WCC"},
            {"rank": 5, "team": "Gonzaga Bulldogs", "w": 9, "l": 6, "col3": 3, "col4": "30", "col5": "+8", "note": "WCC"},
            {"rank": 6, "team": "Portland Pilots", "w": 8, "l": 6, "col3": 4, "col4": "28", "col5": "+6", "note": "WCC"},
            {"rank": 7, "team": "UC Santa Barbara Gauchos", "w": 7, "l": 7, "col3": 4, "col4": "25", "col5": "+1", "note": "Big West"},
            {"rank": 8, "team": "Saint Mary's Gaels", "w": 6, "l": 8, "col3": 3, "col4": "21", "col5": "-4", "note": "WCC"},
            {"rank": 9, "team": "Pacific Tigers", "w": 4, "l": 11, "col3": 2, "col4": "14", "col5": "-18", "note": "WCC"},
        ]
    },
    "cccaa_coast": {
        "title": "CCCAA / 3C2A Coast Conference Football",
        "subtitle": "2026 California Community College Athletic Association",
        "col_headers": ["#", "College", "W", "L", "CONF", "PF", "PA"],
        "rows": [
            {"rank": 1, "team": "San Jose City College Jaguars", "w": 8, "l": 2, "col3": "5-0", "col4": "340", "col5": "185", "note": "Conference Leader"},
            {"rank": 2, "team": "De Anza Mountain Lions", "w": 7, "l": 3, "col3": "4-1", "col4": "310", "col5": "210", "note": "Bowl Contender"},
            {"rank": 3, "team": "Monterey Peninsula Lobos", "w": 6, "l": 4, "col3": "3-2", "col4": "265", "col5": "230", "note": "State Top 20"},
            {"rank": 4, "team": "West Hills Coalinga", "w": 5, "l": 5, "col3": "2-3", "col4": "240", "col5": "250", "note": "Valley Contender"},
            {"rank": 5, "team": "Foothill Owls", "w": 4, "l": 6, "col3": "2-3", "col4": "210", "col5": "260", "note": ""},
            {"rank": 6, "team": "Gavilan Rams", "w": 3, "l": 7, "col3": "1-4", "col4": "185", "col5": "290", "note": ""},
            {"rank": 7, "team": "Hartnell Panthers", "w": 3, "l": 7, "col3": "1-4", "col4": "190", "col5": "280", "note": ""},
            {"rank": 8, "team": "Cabrillo Seahawks", "w": 2, "l": 8, "col3": "0-5", "col4": "160", "col5": "310", "note": ""},
        ]
    },
    "ncaa_water_polo_west": {
        "title": "NCAA Men's Water Polo (MPSF / West)",
        "subtitle": "2026 Collegiate National Rankings",
        "col_headers": ["#", "University", "W", "L", "PCT", "CONF", "STRK"],
        "rows": [
            {"rank": 1, "team": "UCLA Bruins", "w": 21, "l": 2, "col3": ".913", "col4": "5-0", "col5": "W9", "note": "#1 Ranked"},
            {"rank": 2, "team": "California Golden Bears", "w": 19, "l": 4, "col3": ".826", "col4": "4-1", "col5": "W4", "note": "#2 Ranked"},
            {"rank": 3, "team": "Stanford Cardinal", "w": 18, "l": 5, "col3": ".783", "col4": "3-2", "col5": "W2", "note": "#3 Ranked"},
            {"rank": 4, "team": "USC Trojans", "w": 17, "l": 6, "col3": ".739", "col4": "3-2", "col5": "L1", "note": "#4 Ranked"},
            {"rank": 5, "team": "San Jose State Spartans Men", "w": 12, "l": 9, "col3": ".571", "col4": "2-3", "col5": "W1", "note": "#6 Ranked"},
            {"rank": 6, "team": "Santa Clara Broncos Men", "w": 10, "l": 11, "col3": ".476", "col4": "1-4", "col5": "L2", "note": "#10 Ranked"},
            {"rank": 7, "team": "Pacific Tigers", "w": 11, "l": 10, "col3": ".524", "col4": "2-3", "col5": "W1", "note": "#9 Ranked"},
            {"rank": 8, "team": "UC Davis Aggies", "w": 9, "l": 12, "col3": ".429", "col4": "1-4", "col5": "L3", "note": "#12 Ranked"},
        ]
    },
    "ncaa_acc_volleyball": {
        "title": "NCAA Women's Volleyball (ACC Standings)",
        "subtitle": "2026 Atlantic Coast Conference Volleyball",
        "col_headers": ["#", "University", "CONF", "OVR", "PCT", "+/-", "STRK"],
        "rows": [
            {"rank": 1, "team": "Pittsburgh Panthers", "w": 27, "l": 2, "col3": "17-1", "col4": ".931", "col5": "+72", "note": "#1 Seed"},
            {"rank": 2, "team": "Louisville Cardinals", "w": 25, "l": 4, "col3": "16-2", "col4": ".862", "col5": "+59", "note": "#2 Seed"},
            {"rank": 3, "team": "Stanford Cardinal Women", "w": 24, "l": 5, "col3": "15-3", "col4": ".828", "col5": "+55", "note": "#3 Seed"},
            {"rank": 4, "team": "SMU Mustangs", "w": 22, "l": 7, "col3": "14-4", "col4": ".759", "col5": "+41", "note": "NCAA Bid"},
            {"rank": 5, "team": "Georgia Tech Yellow Jackets", "w": 20, "l": 8, "col3": "12-6", "col4": ".714", "col5": "+33", "note": "NCAA Bid"},
            {"rank": 6, "team": "Florida State Seminoles", "w": 19, "l": 9, "col3": "11-7", "col4": ".679", "col5": "+26", "note": "NCAA Bid"},
            {"rank": 7, "team": "North Carolina Tar Heels", "w": 18, "l": 10, "col3": "10-8", "col4": ".643", "col5": "+18", "note": ""},
            {"rank": 8, "team": "Miami Hurricanes", "w": 17, "l": 11, "col3": "9-9", "col4": ".607", "col5": "+10", "note": ""},
        ]
    },
    "ncaa_wcc_hoops": {
        "title": "NCAA Men's Basketball (WCC & NorCal)",
        "subtitle": "2026 West Coast Conference & Regional Standings",
        "col_headers": ["#", "University", "CONF", "OVR", "PCT", "+/-", "STRK"],
        "rows": [
            {"rank": 1, "team": "Gonzaga Bulldogs", "w": 27, "l": 8, "col3": "14-2", "col4": ".771", "col5": "+15.2", "note": "Conference Leader"},
            {"rank": 2, "team": "Saint Mary's Gaels", "w": 26, "l": 8, "col3": "15-1", "col4": ".765", "col5": "+14.8", "note": "NCAA Qualifier"},
            {"rank": 3, "team": "Santa Clara Broncos Men", "w": 21, "l": 13, "col3": "11-5", "col4": ".618", "col5": "+5.4", "note": "WCC Semifinals"},
            {"rank": 4, "team": "San Francisco Dons", "w": 23, "l": 11, "col3": "11-5", "col4": ".676", "col5": "+6.1", "note": "NIT Contender"},
            {"rank": 5, "team": "Loyola Marymount Lions", "w": 15, "l": 17, "col3": "8-8", "col4": ".469", "col5": "-1.2", "note": ""},
            {"rank": 6, "team": "Washington State Cougars", "w": 18, "l": 14, "col3": "9-7", "col4": ".562", "col5": "+2.8", "note": ""},
            {"rank": 7, "team": "Oregon State Beavers", "w": 16, "l": 16, "col3": "7-9", "col4": ".500", "col5": "-0.4", "note": ""},
            {"rank": 8, "team": "Stanislaus State", "w": 14, "l": 14, "col3": "9-9", "col4": ".500", "col5": "-1.0", "note": ""},
        ]
    }
}


def classify_game(game):
    """
    Classifies any game dictionary into one of the 18 standings keys.
    """
    sport = game.get("sport", "")
    level = game.get("level", "")
    league = game.get("league", "")
    home = game.get("home_team", "")
    away = game.get("away_team", "")
    teams_str = f"{home} {away}".lower()
    league_lower = league.lower()

    if sport == "Football":
        if level == "Pro":
            return "nfl_nfc_west"
        elif level == "High School":
            if "de la salle" in teams_str or "ebal" in league_lower or "clovis" in teams_str or "st. mary" in teams_str or "clayton" in teams_str:
                return "hs_ebal"
            elif "wcal" in league_lower or any(x in teams_str for x in ["serra", "saint francis", "bellarmine", "mitty", "valley christian", "riordan"]):
                return "hs_wcal"
            else:
                return "hs_bval"
        elif level == "Junior College":
            return "cccaa_coast"
        elif level == "College":
            if "mountain west" in league_lower or "sjsu" in teams_str or "san jose state" in teams_str:
                return "ncaa_mwc_football"
            else:
                return "ncaa_acc_football"

    elif sport == "Hockey":
        if level == "Minor League" or league == "AHL":
            return "ahl_pacific"
        else:
            return "nhl_pacific"

    elif sport == "Basketball":
        if level == "Pro":
            return "nba_pacific"
        else:
            return "ncaa_wcc_hoops"

    elif sport == "Soccer":
        if "mls next pro" in league_lower or "the town fc" in teams_str:
            return "mls_next_pro_west"
        elif level == "Pro":
            if league == "NWSL":
                return "nwsl"
            else:
                return "mls_west"
        elif level == "Minor League" or league == "USL Championship":
            return "usl_west"
        elif level == "College":
            if "women" in teams_str or "women" in league_lower:
                return "ncaa_west_womens_soccer"
            else:
                return "ncaa_west_mens_soccer"

    elif sport == "Water Polo":
        return "ncaa_water_polo_west"

    elif sport == "Volleyball":
        return "ncaa_acc_volleyball"

    import warnings
    warnings.warn(
        f"classify_game: unrecognized sport/level combination for game id={game.get('id', '?')}: "
        f"sport={game.get('sport', '?')}, level={game.get('level', '?')} — defaulting to nfl_nfc_west",
        stacklevel=2
    )
    return "nfl_nfc_west"


def matches_team_name(name1, name2):
    """
    Fuzzy and exact matcher for team names.
    """
    if not name1 or not name2:
        return False
    n1 = name1.lower().strip()
    n2 = name2.lower().strip()
    if n1 == n2:
        return True
    
    # Common aliases
    aliases = [
        ("49ers", "san francisco 49ers"),
        ("sharks", "san jose sharks"),
        ("warriors", "golden state warriors"),
        ("earthquakes", "san jose earthquakes"),
        ("bay fc", "bay fc"),
        ("roots", "oakland roots sc"),
        ("barracuda", "san jose barracuda"),
        ("stanislaus", "stanislaus state"),
        ("branham", "branham high bruins"),
        ("leigh", "leigh high longhorns"),
        ("serra", "junípero serra padres"),
        ("saint francis", "saint francis lancers"),
        ("de la salle", "de la salle spartans"),
        ("bellarmine", "bellarmine college prep bells"),
        ("mitty", "archbishop mitty monarchs"),
        ("sjcc", "san jose city college jaguars"),
        ("de anza", "de anza mountain lions"),
        ("monterey peninsula", "monterey peninsula lobos"),
        ("stanford", "stanford cardinal"),
        ("cal", "california golden bears"),
        ("san jose state", "san jose state spartans"),
        ("sjsu", "san jose state spartans"),
        ("santa clara", "santa clara broncos"),
    ]
    for short, full in aliases:
        if short in n1 and short in n2:
            # check if both match gender/sport specific if applicable
            if ("women" in n1) != ("women" in n2):
                continue
            return True

    # Substring check
    if n1 in n2 or n2 in n1:
        if ("women" in n1) != ("women" in n2):
            return False
        return True

    return False


def get_standings_for_game(game):
    """
    Returns the enriched standings structure for the provided game dictionary.
    Attaches authentic team logos and highlights `is_home` / `is_away`.
    """
    cat_key = classify_game(game)
    db = get_standings_db()
    standings_meta = db.get(cat_key, db.get("nfl_nfc_west", STANDINGS_DATABASE["nfl_nfc_west"]))
    
    home_name = game.get("home_team", "")
    away_name = game.get("away_team", "")

    enriched_rows = []
    home_matched = False
    away_matched = False

    for row in standings_meta["rows"]:
        r = dict(row)
        team_name = r["team"]
        
        # Attach logo
        r["logo"] = team_logos.get_team_logo(team_name)
        
        # Check match with home/away
        is_h = matches_team_name(team_name, home_name)
        is_a = matches_team_name(team_name, away_name)

        if is_h:
            r["is_home"] = True
            r["highlight_tag"] = "HOME"
            home_matched = True
        elif is_a:
            r["is_away"] = True
            r["highlight_tag"] = "AWAY"
            away_matched = True
        else:
            r["is_home"] = False
            r["is_away"] = False
            r["highlight_tag"] = ""

        enriched_rows.append(r)

    # Check if away or home team was an out-of-division guest opponent
    guest_notes = []
    cross_opps = standings_meta.get("cross_division_opponents", {})

    if not away_matched and away_name:
        opp_info = None
        for k, v in cross_opps.items():
            if matches_team_name(k, away_name):
                opp_info = (k, v)
                break
        if opp_info:
            k, v = opp_info
            guest_notes.append({
                "team": away_name,
                "role": "AWAY",
                "logo": team_logos.get_team_logo(away_name),
                "division": v.get("division", "Non-Division"),
                "record": v.get("record", f"{v.get('w')}-{v.get('l')}"),
                "rank": v.get("rank", "Contender")
            })

    if not home_matched and home_name:
        opp_info = None
        for k, v in cross_opps.items():
            if matches_team_name(k, home_name):
                opp_info = (k, v)
                break
        if opp_info:
            k, v = opp_info
            guest_notes.append({
                "team": home_name,
                "role": "HOME",
                "logo": team_logos.get_team_logo(home_name),
                "division": v.get("division", "Non-Division"),
                "record": v.get("record", f"{v.get('w')}-{v.get('l')}"),
                "rank": v.get("rank", "Contender")
            })

    return {
        "key": cat_key,
        "title": standings_meta["title"],
        "subtitle": standings_meta["subtitle"],
        "col_headers": standings_meta["col_headers"],
        "rows": enriched_rows,
        "guest_notes": guest_notes,
        "home_matched": home_matched,
        "away_matched": away_matched
    }


if __name__ == "__main__":
    import build_calendar
    games = build_calendar.GAMES_DATA
    print(f"Testing standings engine across all {len(games)} games...")
    unmatched_home = []
    unmatched_away = []
    
    for g in games:
        st = get_standings_for_game(g)
        assert st["title"], f"Game {g['id']} has no standings title"
        assert len(st["rows"]) >= 4, f"Game {g['id']} has less than 4 rows"
        
        # Verify logos on all rows
        for r in st["rows"]:
            assert r["logo"], f"Row {r['team']} in {st['title']} missing logo"

        if not st["home_matched"]:
            unmatched_home.append((g["id"], g["home_team"], st["key"]))
        if not st["away_matched"]:
            unmatched_away.append((g["id"], g["away_team"], st["key"]))

    print(f"Standings engine tested!")
    print(f"Unmatched Home ({len(unmatched_home)}): {unmatched_home}")
    print(f"Unmatched Away ({len(unmatched_away)}): {unmatched_away}")
