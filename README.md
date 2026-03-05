# External Data -> Transform -> BI (Example Project)

This repository demonstrates an end-to-end analytics workflow: collecting external web data, transforming text-based play-by-play into structured metrics, and exposing the results to BI dashboards.
(Example source used here: Basketball Reference play-by-play pages.)

**TL;DR:** Basketball Reference provides play-by-play as text events. This project converts those events into player/team metrics (shots, free throws, scoring splits, opponent context, etc.) and visualizes them in Power BI.

### Raw Data
![Basketball Reference](https://github.com/gustavo-alvarenga/About-me/blob/main/NBA%20Raw%20Data.png)

### BI Dashboard (Example) (Click to view the interactive [dashboard](https://app.powerbi.com/view?r=eyJrIjoiZWVmYzRkYjAtMTU3OS00YTNhLWEzYTctMjA5M2U5OTE1NDU0IiwidCI6ImE2ZThmZmUwLTg1ZWYtNDBhMS1iMDU1LTUxNmU2YjY1ODJmMiJ9))
![Twitch](https://github.com/Gus-Alvarenga/About-me/blob/main/nba%20dashboard.png)

### Tech Stack:
* Python
* Power BI

## Architecture (High Level)

**Flow**
1. **Collect (rate-limited):** Gather game URLs for a season/date range.
2. **Extract:** Download play-by-play pages and parse text events into structured rows.
3. **Transform:** Convert rows into analytics-ready metrics (player/team aggregates, splits, and derived fields).
4. **Serve (BI):** Load outputs into Power BI for modeling and visualization.

Source pages -> link list -> play-by-play extraction -> metrics tables (CSV) -> Power BI

## Repository Contents

- `collect_game_links.py` - Builds a list of game URLs for a selected date range/season.
- `extract_transform_pbp.py` - Downloads play-by-play pages and transforms text events into structured metrics tables.
- `enrich_player_metadata.py` - Extracts unique players from play-by-play and adds metadata for analysis.
- `README.md` - Project overview and setup instructions.

## Quickstart (Reproducible Setup)

1. Create a virtual environment
   - `python -m venv .venv`
   - `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)

2. Install dependencies
   - `pip install -r requirements.txt`

3. Run the pipeline
   - `python collect_game_links.py`
   - `python extract_transform_pbp.py`
   - `python enrich_player_metadata.py`

## Required Configuration

At minimum, you will need to set:
- Season/date range parameters (as used in `collect_game_links.py`)
- Output folder paths (if your scripts write files locally)

Notes:
- This project uses rate limiting to respect source-site request limits.

## Step #1: Retrieve List of Links

This step builds the list of game URLs starting from a selected season start date and continuing forward.

Code: [collect_game_links.py](https://github.com/Gus-Alvarenga/NBA/blob/main/collect_game_links.py)

Notes:
- Requests are rate-limited to respect Basketball Reference limits (10 requests/min at the time of writing). You can check this information [here](https://www.sports-reference.com/bot-traffic.html).
- Outputs are saved locally for downstream steps.

## Step #2: Retrieve and Process Data

This step downloads play-by-play pages and converts text-based events into structured rows, then aggregates them into analytics-ready metrics.

Code: [extract_transform_pbp.py](https://github.com/Gus-Alvarenga/NBA/blob/main/extract_transform_pbp.py)

Process Workflow:
* Read game URL list
* Download play-by-play pages (rate-limited)
* Parse text events into structured records
* Generate metrics tables (CSV outputs) for BI

## Step #3: Players Metadata

This step extracts unique players from the play-by-play dataset and enriches the analysis with additional player metadata.

Code: [enrich_player_metadata.py](https://github.com/Gus-Alvarenga/NBA/blob/main/enrich_player_metadata.py)

## Step #4: Visualization

Load the curated CSV outputs into Power BI, model relationships as needed, and build dashboards.

This example dashboard focuses on:
- Player performance (overall + splits)
- Free throw accuracy (by attempt number)
- Performance vs different opponents
- Scoring by distance from the arc

Dashboard: [dashboard](https://app.powerbi.com/view?r=eyJrIjoiZWVmYzRkYjAtMTU3OS00YTNhLWEzYTctMjA5M2U5OTE1NDU0IiwidCI6ImE2ZThmZmUwLTg1ZWYtNDBhMS1iMDU1LTUxNmU2YjY1ODJmMiJ9)  
![NBA](https://github.com/Gus-Alvarenga/About-me/blob/main/nba%20dashboard.png)

You can reach out to me on [LinkedIn](https://www.linkedin.com/in/gus-alvarenga/)
