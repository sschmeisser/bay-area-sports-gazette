# The Bay Area Sports Gazette

> **A curated 7-day weekly schedule, scores archive, and insider almanac covering Professional, Collegiate (NCAA D1), Junior College (3C2A), and High School athletics across San Jose, the South Bay, Peninsula, East Bay, and Monterey.**

---

## 🌟 Live Endpoints

- **Primary Custom Shortlink**: [tinyurl.com/bay-sports-live](https://tinyurl.com/bay-sports-live)
- **Alternate Custom Shortlinks**:
  - [tinyurl.com/bay-sports-hub](https://tinyurl.com/bay-sports-hub)
  - [tinyurl.com/bay-sports-scores](https://tinyurl.com/bay-sports-scores)
  - [tinyurl.com/sj-sports-today](https://tinyurl.com/sj-sports-today)
- **Direct Cloud CDN Deployment**: [https://azure-sorbet-3br8.here.now/](https://azure-sorbet-3br8.here.now/)

---

## 🏈 Comprehensive Team & League Coverage (85 Teams)

### 1. High School Athletics (20 Programs with Official School Emblems)
- **WCAL**: Archbishop Mitty, Bellarmine College Prep, Junípero Serra, Saint Francis, Valley Christian
- **BVAL**: Branham High, Leigh High, Leland, Live Oak, Piedmont Hills, Pioneer, Santa Teresa, Westmont, Willow Glen
- **EBAL / SFL / CIF Showcase**: Clayton Valley Charter, Clovis North, De La Salle, Folsom, McClymonds, St. Mary's (Stockton)

### 2. Major Professional Sports
- **NFL**: San Francisco 49ers (plus Arizona Cardinals, Dallas Cowboys, LA Rams, New Orleans Saints, Seattle Seahawks)
- **NHL**: San Jose Sharks, Anaheim Ducks, Calgary Flames, Edmonton Oilers, LA Kings, Seattle Kraken, Vegas Golden Knights
- **NBA**: Golden State Warriors, Denver Nuggets, LA Lakers
- **MLS**: San Jose Earthquakes, LA Galaxy, Portland Timbers, Real Salt Lake, Seattle Sounders, Vancouver Whitecaps
- **NWSL**: Bay FC, Angel City FC, Chicago Red Stars, NJ/NY Gotham FC, Seattle Reign FC
- **USL Championship**: Oakland Roots SC, Monterey Bay FC, Sacramento Republic FC, Orange County SC, Phoenix Rising, San Antonio FC, El Paso Locomotive
- **AHL**: San Jose Barracuda, Ontario Reign

### 3. Collegiate NCAA Division I
- Stanford Cardinal (Football, Men's & Women's Soccer, Volleyball, Basketball)
- California Golden Bears (Football, Men's Soccer, Basketball)
- San Jose State Spartans (Football, Men's Soccer, Water Polo)
- Santa Clara Broncos (Men's & Women's Soccer)
- Air Force Falcons, Minnesota Golden Gophers, San Diego State, Syracuse, Washington, etc.

### 4. Junior College (CCCAA / 3C2A)
- San Jose City College (SJCC Jaguars)
- De Anza Mountain Lions (Cupertino)
- Gavilan Rams (Gilroy)
- Monterey Peninsula College (MPC Lobos)
- West Hills Coalinga

---

## 📱 Mobile-First Ergonomic UX & Features

- **Thumb-Zone Bottom Dock**: Quick access to Schedule, Agenda continuous stream, Filter modal, and My Plan with live badge counter.
- **Scroll-Contained Stepper**: Fixed `←` and `→` boundary buttons with auto-centering active week pills (`Past Week (Scores)`, `Week 1`, `Week 2`, `Week 3`, `Week 4`, `Week 5`, `Week 6`).
- **Strict Single-Day Swipe Navigation**: Gesture isolation with cooldown debounce prevents accidental multi-day skipping while keeping the background locked in place (`overflow-x: clip; touch-action: pan-y`).
- **Official Team Logos**: 100% verified, crisp transparent PNGs for all 47 Pro & NCAA D1 programs (ESPN CDN) and all 20 High Schools (official MaxPreps/athletics assets), with bespoke vector SVG shields for minor leagues and junior colleges.
- **Native Slide-Up Bottom Sheets**: High-polish game detail sheets with dual-crest matchup headers, ticket links, gameday context, and local insider guides (parking, food, student sections).
- **Personalized "My Plan" Feed**: Save games with 1 tap; generate and download instant `.ics` calendar feeds for Apple Calendar, Google Calendar, and Outlook.
- **Rolling Scores & Results Archive**: View previous week final scores, winner highlights (`✓`), and postgame recaps.

---

## 🛠️ Quickstart & Local Development

### 1. Rebuild the Calendar
```bash
python3 build_calendar.py
```
This generates `sports_calendar.html` and synchronizes `index.html` in `<0.05s`.

### 2. Run Local Development Server
```bash
python3 serve.py
```
Serves the application locally on `http://localhost:8999`.

---

## 📁 Repository Structure

```
bay-area-sports-gazette/
├── assets/
│   └── hs_logos/               # 20 official high school transparent PNG logos
├── build_calendar.py           # Master compiler & game schedule generator
├── calendar_template.html      # Responsive editorial layout & mobile UX logic
├── team_logos.py               # Logo registry with base64 fallbacks & color palettes
├── serve.py                    # Lightweight local HTTP preview server
├── local_sports_schedule.md    # 102-team editorial directory & almanac
├── requirements.txt            # Python dependencies
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for full text.

## ⚠️ Trademark Disclaimer

All team names, logos, and trademarks featured on this site belong to their respective owners (NFL, NHL, NBA, MLS, NWSL, USL Championship, NCAA, and individual clubs). This project is an independent fan community resource created for non-commercial, educational, and entertainment purposes. It is not affiliated with, endorsed by, or sponsored by any professional or collegiate sports organization.
