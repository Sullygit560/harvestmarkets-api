from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import glob
import os

app = FastAPI()

# Enable CORS so frontend can fetch from backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/latest-score")
def get_latest_score():
    try:
        # Look for the latest *_score.csv file in daily_scores/
        score_files = glob.glob("daily_scores/*_score.csv")
        if not score_files:
            raise FileNotFoundError("No score files found in daily_scores/")

        latest_file = max(score_files, key=os.path.getctime)

        df = pd.read_csv(latest_file)
        latest = df.iloc[-1].to_dict()

        # Optional: Restructure output
        score_data = {
            "date": latest["date"],
            "scores": {
                "price": latest.get("price_score"),
                "cot": latest.get("cot_score"),
                "weather": latest.get("weather_score"),
                "export": latest.get("export_score"),
                "technical": latest.get("technical_score"),
                "news": 50  # placeholder until real news sentiment is added
            }
        }

        return score_data

    except Exception as e:
        return {"error": str(e)}
