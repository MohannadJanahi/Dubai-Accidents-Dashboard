# Dubai Traffic Accidents Dashboard

An interactive dashboard for exploring traffic accident patterns in Dubai built to help identify when, where, and how severely accidents cluster across the city, to support road safety analysis and resource planning.

<img width="1915" height="567" alt="Screenshot from 2026-06-29 00-24-38" src="https://github.com/user-attachments/assets/e9818dd4-435f-4e4a-9800-736676b75660" />

## Problem

Traffic accident data on its own is just rows in a spreadsheet. It doesn't reveal patterns like "accidents spike during evening rush hour" or "high-severity incidents cluster in specific districts." This dashboard turns Dubai's open traffic incident data into an interactive map so those spatial and temporal patterns are immediately visible, instead of requiring a manual query for every question.

## Features

- **Interactive map** of accident locations across Dubai, color-coded by severity (Low / High)
- **Time-of-day filter**: view accidents by morning, afternoon, evening, and/or night, individually or combined
- **Severity filter**: isolate low-severity or high-severity incidents, or view both
- **Month/year filter**: dynamically populated based on your other filter selections, so you only see time periods with matching data
- **"Past week" toggle**: quickly jump to the most recent week of data relative to the latest record
- Hover tooltips showing the day, month, and year of each incident

## Data

Source: [Dubai Pulse — Traffic Incidents](https://www.dubaipulse.gov.ae/data/dp-traffic/dp_traffic_incidents-open)

By default, the dashboard uses a bundled local CSV snapshot (`Datasets/Accidents.csv`) for offline and reproducible use. Pass `--online` to fetch the latest data from Dubai Pulse instead. Each record includes incident time, location coordinates, and a severity classification (the raw severity field is bilingual — Arabic/English — and is normalized during preprocessing).

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
# Fetch the latest data from Dubai Pulse
python dashboard.py --online

# Use a specific CSV file
python dashboard.py --data path/to/Accidents.csv

# Change host, port, or enable debug mode
python dashboard.py --host 0.0.0.0 --port 8080 --debug
```

## Tech Stack

Python, Dash, Plotly Express, pandas
