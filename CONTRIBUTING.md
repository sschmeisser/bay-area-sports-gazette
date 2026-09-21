# Contributing to Bay Area Sports Gazette

Thank you for your interest in contributing! This guide covers everything you need to get started.

---

## 📋 Table of Contents

1. [Updating Game Data](#1-updating-game-data)
2. [Building Locally](#2-building-locally)
3. [Verifying Schedule Data](#3-verifying-schedule-data)
4. [Running a Local Server](#4-running-a-local-server)
5. [Submitting a Pull Request](#5-submitting-a-pull-request)
6. [Trademark Notice](#6-trademark-notice)

---

## 1. Updating Game Data

All game schedule data lives in the `GAMES_DATA` list inside [`build_calendar.py`](build_calendar.py).

Each entry is a Python dictionary with fields such as:

```python
{
    "date": "2026-09-20",          # ISO 8601 date
    "time": "7:30 PM",             # Local kickoff/tip-off time (Pacific)
    "home_team": "San Jose Earthquakes",
    "away_team": "LA Galaxy",
    "sport": "Soccer",
    "league": "MLS",
    "venue": "PayPal Park",
    "ticket_url": "https://...",   # Optional
    "notes": "Derby match",        # Optional
}
```

To add a game:
1. Open `build_calendar.py` in your editor.
2. Locate the `GAMES_DATA` list (search for `GAMES_DATA = [`).
3. Insert a new dictionary entry in chronological order.
4. Save the file and rebuild (see step 2 below).

To remove or correct a game, simply delete or edit the corresponding dictionary entry.

---

## 2. Building Locally

After editing `build_calendar.py`, regenerate the output bundle:

```bash
python3 build_calendar.py
```

This produces `index.html` (and `sports_calendar.html`) in the repository root. Open either file directly in a browser to preview your changes.

**Requirements**: Python 3.9 or later. No additional packages are needed for the build step itself.

---

## 3. Verifying Schedule Data

If `schedule_fetcher.py` is present in the repository, you can run a data-integrity check against live sources:

```bash
python3 schedule_fetcher.py --verify
```

This script is optional and may require the `requests` package:

```bash
pip install -r requirements.txt
```

---

## 4. Running a Local Server

For accurate relative-path resolution (and to avoid browser CORS restrictions on `file://`), serve the project with Python's built-in HTTP server:

```bash
python3 -m http.server 8080
```

Then open **http://localhost:8080** in your browser.

Alternatively, `serve.py` provides a local server plus an optional Cloudflare quick-tunnel for sharing a live preview URL:

```bash
python3 serve.py
```

---

## 5. Submitting a Pull Request

1. **Fork** this repository on GitHub.
2. **Clone** your fork and create a feature branch:
   ```bash
   git clone https://github.com/<your-username>/bay-area-sports-gazette.git
   cd bay-area-sports-gazette
   git checkout -b fix/add-sjsu-game-oct12
   ```
3. **Update** the `GAMES_DATA` list (or other source files) as needed.
4. **Rebuild** the output:
   ```bash
   python3 build_calendar.py
   ```
5. **Commit both** the source change and the regenerated output:
   ```bash
   git add build_calendar.py index.html sports_calendar.html
   git commit -m "feat: add SJSU vs. Nevada Oct 12"
   ```
6. **Push** your branch and open a Pull Request against `main`.

Please keep PRs focused — one logical change per PR makes review much easier.

---

## 6. Trademark Notice

All team names, logos, and trademarks displayed in this project belong to their respective owners (the NFL, NBA, NHL, MLS, NWSL, NCAA, individual schools, and other organizations). They are used here solely for non-commercial, fan-community, and local sports promotion purposes. This project is not affiliated with, endorsed by, or sponsored by any of those organizations.
