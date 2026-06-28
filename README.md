# Dubai Traffic Accidents Dashboard

An interactive dashboard for exploring traffic accident patterns in Dubai — built to help identify when, where, and how severely accidents cluster across the city, to support road safety analysis and resource planning.

![Dashboard preview](docs/preview.png)
*(add a screenshot or short GIF of the map with filters applied)*

## Problem

Traffic accident data on its own is just rows in a spreadsheet — it doesn't reveal patterns like "accidents spike during evening rush hour" or "high-severity incidents cluster in specific districts." This dashboard turns Dubai's open traffic incident data into an interactive map so those spatial and temporal patterns are immediately visible, instead of requiring a manual query for every question.

## Features

- **Interactive map** of accident locations across Dubai, color-coded by severity (Low / High)
- **Time-of-day filter** — view accidents by morning, afternoon, evening, and/or night, individually or combined
- **Severity filter** — isolate low-severity or high-severity incidents, or view both
- **Month/year filter** — dynamically populated based on your other filter selections, so you only see time periods with matching data
- **"Past week" toggle** — quickly jump to the most recent week of data relative to the latest record
- Hover tooltips showing the day, month, and year of each incident

## Data

Source: [Dubai Pulse — Traffic Incidents](https://www.dubaipulse.gov.ae/data/dp-traffic/dp_traffic_incidents-open)

The dashboard can pull live data directly from Dubai Pulse, or run against a bundled local CSV snapshot (`Datasets/Accidents.csv`) for offline/reproducible use. Each record includes incident time, location coordinates, and a severity classification (the raw severity field is bilingual — Arabic/English — and is normalized during preprocessing).

## Results / Insights

*(Add 2-3 sentences here on what you actually noticed using the dashboard — e.g. which time periods or areas show the most incidents, or how the high vs. low severity split looks across the city. This is the part that turns it from "a dashboard" into "an analysis," so it's worth filling in before this is finished.)*

## How to Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python dashboard.py
```

Open `http://127.0.0.1:8050` in your browser.

### Options

```bash
# Use the bundled local dataset instead of downloading from Dubai Pulse
python dashboard.py --data local

# Use a specific CSV file
python dashboard.py --data Datasets/Accidents.csv

# Change host, port, or enable debug mode
python dashboard.py --host 0.0.0.0 --port 8080 --debug
```

## Tech Stack

Python, Dash, Plotly Express, pandas, GeoPandas
