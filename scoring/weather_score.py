import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta, UTC

def score_weather():
    # 🌍 Regional coverage
    stations = [
        "KMSP", "KCMI", "KDSM", "KOMA", "KMKC", "KSTL", "KDVN", "KMDH",  # Core Corn Belt
        "KDDC", "KSLN", "KGRI", "KFSD", "KFAR", "KGDB",                  # Plains & North
        "KALO", "KMPZ", "KEVV", "KDEC", "KRFD", "KMQB", "KFWA", "KLAF", "KCMH"  # Expanded Midwest
    ]

    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=3)

    base_url = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
    params = {
        "station": stations,
        "data": "tmpf,relh,precip",
        "tz": "Etc/UTC",
        "format": "comma",
        "latlon": "no",
        "missing": "empty",
        "trace": "0.0001",
        "year1": start_date.year,
        "month1": start_date.month,
        "day1": start_date.day,
        "year2": end_date.year,
        "month2": end_date.month,
        "day2": end_date.day,
    }

    response = requests.get(base_url, params=params)
    if not response.ok:
        raise Exception(f"Failed to fetch IEM data: {response.status_code}")

    clean_lines = [
        line for line in response.text.splitlines()
        if not line.startswith("#") and "DEBUG" not in line
    ]

    if not clean_lines or "station,valid" not in clean_lines[0]:
        raise ValueError("No valid CSV header found")

    df = pd.read_csv(StringIO("\n".join(clean_lines)), on_bad_lines="skip")
    df = df.dropna(subset=["tmpf"])

    if df.empty:
        raise ValueError("No temperature readings in dataset")

    # 🌡️ Calculate average temperature
    avg_temp = df["tmpf"].astype(float).mean()

    # 🌧️ Sum precipitation (if available)
    if "precip" in df.columns:
        total_precip = df["precip"].astype(float).sum()
    else:
        total_precip = 0.0

    # 🧮 Scoring logic (adjust as needed)
    temp_penalty = max(0, avg_temp - 90) * 1.5  # Penalize heat
    precip_bonus = min(total_precip, 1.0) * 5   # Reward moisture

    raw_score = 50 - temp_penalty + precip_bonus
    score = round(min(max(raw_score, 0), 100), 2)

    return score

