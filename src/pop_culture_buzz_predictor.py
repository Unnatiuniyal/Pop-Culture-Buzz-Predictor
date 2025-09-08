import os, time
import numpy as np
import pandas as pd
from pytrends.request import TrendReq
from prophet import Prophet
import matplotlib.pyplot as plt

# -----------------------------
# Config
# -----------------------------
DATA_DIR = "data/raw"
CLEAN_PATH = "data/google_trends_clean.csv"
FORECAST_DIR = "data/forecasts_prophet"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FORECAST_DIR, exist_ok=True)

anchor = "Instagram"
keywords = [
    'Rihanna', 'Kendrick Lamar', 'Taylor Swift', 'Travis Scott', 'BTS',
    'Blackpink', 'Doja Cat', 'Olivia Rodrigo', 'Zendaya', 'Jenna Ortega',
    'Wednesday', 'Stranger Things'
]

TIMEFRAME = "today 12-m"
SLEEP_BETWEEN = 30
RETRIES = 3

# -----------------------------
# Fetch trends
# -----------------------------
def fetch_pair_ratio(kw, anchor, retries=RETRIES, sleep_time=SLEEP_BETWEEN):
    pytrends = TrendReq(hl="en-US", tz=360)
    for attempt in range(1, retries+1):
        try:
            pytrends.build_payload([kw, anchor], timeframe=TIMEFRAME)
            df = pytrends.interest_over_time().drop(columns=["isPartial"], errors="ignore")
            if df.empty:
                return None
            denom = df[anchor].replace(0, np.nan)
            ratio = 100.0 * (df[kw] / denom)
            ratio = ratio.interpolate(limit_direction="both").fillna(0.0)
            ratio.name = kw
            return ratio
        except Exception as e:
            print(f"Error fetching {kw} (attempt {attempt}): {e}")
            time.sleep(sleep_time * attempt)
    return None

def collect_trends(keywords, anchor):
    series_list = []
    for kw in keywords:
        s = fetch_pair_ratio(kw, anchor)
        if s is not None:
            series_list.append(s)
        time.sleep(SLEEP_BETWEEN)
    combined = pd.concat(series_list, axis=1)
    combined.index.name = "date"
    return combined

# -----------------------------
# Cleaning + smoothing
# -----------------------------
def clean_data(path_in, path_out=CLEAN_PATH):
    df = pd.read_csv(path_in, parse_dates=["date"])
    df_clean = (
        df.set_index("date")
          .replace(0, np.nan)
          .interpolate(method="linear", limit_direction="both")
          .rolling(window=7, min_periods=1)
          .mean()
          .reset_index()
    )
    df_clean.to_csv(path_out, index=False)
    return df_clean

# -----------------------------
# Forecast
# -----------------------------
def forecast_artist(series, horizon=12):
    s = series.reset_index().rename(columns={"date":"ds", series.name:"y"})
    s["y"] = s["y"].clip(lower=0)
    m = Prophet(weekly_seasonality=True)
    m.fit(s)
    future = m.make_future_dataframe(periods=horizon, freq="W")
    fcst = m.predict(future)

    out_csv = os.path.join(FORECAST_DIR, f"{series.name}_forecast.csv")
    fcst.to_csv(out_csv, index=False)
    return fcst
