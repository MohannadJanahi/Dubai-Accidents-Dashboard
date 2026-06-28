# Dubai-Accidents-Dashboard
An interactive dashboard to visualize traffic accidents in the city of Dubai within the past year

Data provided by https://www.dubaipulse.gov.ae/data/dp-traffic/dp_traffic_incidents-open

## Run the dashboard

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python dashboard.py
```

Open http://127.0.0.1:8050 in your browser.

### Options

```bash
# Use the bundled local dataset instead of downloading from Dubai Pulse
python dashboard.py --data local

# Use a specific CSV file
python dashboard.py --data Datasets/Accidents.csv

# Change host, port, or enable debug mode
python dashboard.py --host 0.0.0.0 --port 8080 --debug
```
