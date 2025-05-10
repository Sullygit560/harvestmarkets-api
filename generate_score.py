from datetime import datetime, UTC
import os
import pandas as pd

from scoring.price_score import score_price
from scoring.cot_score import score_cot
from scoring.weather_score import score_weather
from scoring.export_score import score_export
from scoring.technical_score import score_technical
from scoring.apply_boosts import apply_boost

def normalize(value, min_val=0, max_val=10):
    """Scales any value to 0–100 range."""
    return round((value - min_val) / (max_val - min_val) * 100, 2)

def generate_score():
    os.makedirs("daily_scores", exist_ok=True)

    # Fetch raw scores from component functions
    raw_scores = {
        "price": score_price(),         # assumed 0–10
        "cot": None,
        "weather": score_weather(),     # assumed 0–100
        "export": score_export(),       # assumed 0–10
        "technical": score_technical()  # assumed 0–10
    }

    cot_score, cot_weighted = score_cot()
    raw_scores["cot"] = cot_score

    # Normalize each score to a 0–100 scale
    normalized_scores = {
        "price": normalize(raw_scores["price"]),
        "cot": normalize(raw_scores["cot"]),
        "weather": raw_scores["weather"],
        "export": normalize(raw_scores["export"]),
        "technical": normalize(raw_scores["technical"])
    }

    # Only the total score is boosted — components remain clean
    boosted_score = apply_boost(normalized_scores)

    # Full output for CSV logging
    full_output = {
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
        **normalized_scores,
        "cot_weighted": cot_weighted,
        "total_score": round(boosted_score, 2)
    }

    pd.DataFrame([full_output]).to_csv(f"daily_scores/{full_output['date']}_score.csv", index=False)

    # Return values for API
    return normalized_scores, boosted_score
