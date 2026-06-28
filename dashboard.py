"""Interactive dashboard for Dubai traffic accident data."""

import argparse
from pathlib import Path

import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

DEFAULT_DATA_URL = (
    "https://www.dubaipulse.gov.ae/dataset/c9263194-5ee3-4340-b7c0-3269b26acb43/"
    "resource/c3ece154-3071-4116-8650-e769d8416d88/download/traffic_incidents.csv"
)
DEFAULT_LOCAL_DATA = Path(__file__).resolve().parent / "Datasets" / "Accidents.csv"


def get_hours_for_time_periods(time_periods):
    hours = []
    if "morning" in time_periods:
        hours += list(range(6, 12))
    if "afternoon" in time_periods:
        hours += list(range(12, 18))
    if "evening" in time_periods:
        hours += list(range(18, 24))
    if "night" in time_periods:
        hours += list(range(0, 6))
    return hours


def normalize_severity(value: str) -> str:
    value = str(value).strip()
    if value in {"Low", "بسيط"}:
        return "Low"
    if value in {"High", "خطير"}:
        return "High"
    return value


def load_and_prepare_data(source: str) -> pd.DataFrame:
    df = pd.read_csv(source)
    df["severity"] = (
        df["acci_name"].str.split("-").str[-1].map(normalize_severity)
    )
    df.dropna(inplace=True)

    if "/" in str(df["acci_time"].iloc[0]):
        df["acci_time"] = pd.to_datetime(df["acci_time"], dayfirst=True)
    else:
        df["acci_time"] = pd.to_datetime(df["acci_time"])
    df["hour"] = df["acci_time"].dt.hour
    df["day_of_week"] = df["acci_time"].dt.day_name()
    df["year"] = df["acci_time"].dt.year
    df["month"] = df["acci_time"].dt.month
    df["day"] = df["acci_time"].dt.day
    )
    return df


def create_app(df: pd.DataFrame) -> dash.Dash:
    app = dash.Dash(__name__)

    app.layout = html.Div(
        [
            html.H1("Traffic Accidents Dashboard"),
            dcc.Dropdown(
                id="time-period",
                options=[
                    {"label": "Morning (6am - 12pm)", "value": "morning"},
                    {"label": "Afternoon (12pm - 6pm)", "value": "afternoon"},
                    {"label": "Evening (6pm - 12am)", "value": "evening"},
                    {"label": "Night (12am - 6am)", "value": "night"},
                ],
                value=["morning", "afternoon", "evening", "night"],
                multi=True,
                placeholder="Select time period(s)",
            ),
            dcc.Dropdown(
                id="severity",
                options=[
                    {"label": "Low Severity", "value": "Low"},
                    {"label": "High Severity", "value": "High"},
                    {"label": "Both", "value": "both"},
                ],
                value="both",
                placeholder="Select severity",
            ),
            dcc.Dropdown(
                id="month-year",
                multi=True,
                placeholder="Select month(s) and year(s)",
            ),
            dcc.Checklist(
                id="past-week-checkbox",
                options=[{"label": "Show past week data", "value": "show_past_week"}],
                value=[],
            ),
            dcc.Graph(id="map-graph"),
        ]
    )

    @app.callback(
        Output("month-year", "options"),
        [Input("time-period", "value"), Input("severity", "value")],
    )
    def populate_month_year_dropdown(time_periods, severity):
        filtered_df = df[df["hour"].isin(get_hours_for_time_periods(time_periods))]

        if severity != "both":
            filtered_df = filtered_df[filtered_df["severity"] == severity]

        unique_years_months = filtered_df["acci_time"].dt.strftime("%Y-%m").unique()
        return [{"label": ym, "value": ym} for ym in unique_years_months]

    @app.callback(
        Output("map-graph", "figure"),
        [
            Input("time-period", "value"),
            Input("severity", "value"),
            Input("month-year", "value"),
            Input("past-week-checkbox", "value"),
        ],
    )
    def update_map(time_periods, severity, month_years, past_week_checkbox):
        filtered_df = df[df["hour"].isin(get_hours_for_time_periods(time_periods))]

        if severity != "both":
            filtered_df = filtered_df[filtered_df["severity"] == severity]

        if month_years:
            filtered_df = filtered_df[
                filtered_df["acci_time"].dt.strftime("%Y-%m").isin(month_years)
            ]

        if "show_past_week" in past_week_checkbox:
            latest_date = df["acci_time"].max()
            past_week_date = latest_date - pd.Timedelta(days=7)
            filtered_df = filtered_df[filtered_df["acci_time"] >= past_week_date]

        return px.scatter_mapbox(
            filtered_df,
            lat="acci_x",
            lon="acci_y",
            color="severity",
            mapbox_style="carto-positron",
            zoom=10,
            hover_data={
                "day": True,
                "month": True,
                "year": True,
                "acci_x": False,
                "acci_y": False,
            },
        )

    return app


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Dubai traffic accidents dashboard.")
    parser.add_argument(
        "--data",
        default=DEFAULT_DATA_URL,
        help="CSV file path or URL for traffic incident data.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the server to.")
    parser.add_argument("--port", type=int, default=8050, help="Port to bind the server to.")
    parser.add_argument("--debug", action="store_true", help="Run Dash in debug mode.")
    return parser.parse_args()


def main():
    args = parse_args()
    data_source = args.data

    if data_source == "local" and DEFAULT_LOCAL_DATA.exists():
        data_source = str(DEFAULT_LOCAL_DATA)

    print(f"Loading data from {data_source}...")
    df = load_and_prepare_data(data_source)
    print(f"Loaded {len(df):,} records.")

    app = create_app(df)
    print(f"Starting dashboard at http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
