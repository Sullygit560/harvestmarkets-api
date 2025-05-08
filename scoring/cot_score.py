# scoring/score_cot.py

import requests
import pandas as pd
import zipfile
import io
import csv
from datetime import datetime

def score_cot():
    try:
        today = datetime.utcnow()
        cot_url = f"https://www.cftc.gov/files/dea/history/fut_disagg_txt_{today.year}.zip"

        print(f"📦 Trying COT ZIP: {cot_url}")
        response = requests.get(cot_url)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            fname = [f for f in z.namelist() if f.endswith(".txt")][0]
            with z.open(fname) as f:
                decoded = io.StringIO(f.read().decode("utf-8"))
                reader = csv.reader(decoded)
                rows = list(reader)

        headers = rows[0]
        data_rows = rows[1:]
        df = pd.DataFrame(data_rows, columns=headers)

        print("✅ Parsed COT columns:")
        print(df.columns.tolist())

        # 🧽 Filter for corn contracts
        corn_df = df[df["Market_and_Exchange_Names"].str.contains("CORN", case=False, na=False)].copy()
        corn_df["Report_Date_as_YYYY-MM-DD"] = pd.to_datetime(corn_df["Report_Date_as_YYYY-MM-DD"], errors="coerce")

        # ⏳ Use most recent available report
        latest_date = corn_df["Report_Date_as_YYYY-MM-DD"].max()
        latest = corn_df[corn_df["Report_Date_as_YYYY-MM-DD"] == latest_date]

        # 💹 Extract M.Money long/short
        short = float(latest["M_Money_Positions_Short_All"].values[0])
        long = float(latest["M_Money_Positions_Long_All"].values[0])
        net = long - short

        cot_score = round(net / 10000, 2)
        cot_weighted = round(cot_score * 0.6, 2)

        return cot_score, cot_weighted

    except Exception as e:
        print(f"❌ Error scoring COT: {e}")
        return None, None
