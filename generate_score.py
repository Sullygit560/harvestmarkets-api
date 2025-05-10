# generate_score.py

import os
from datetime import datetime, UTC
from scoring.price_score import score_price
from scoring.cot_score import score_cot
from scoring.weather_score import score_weather
from scoring.export_score import score_export
from scoring.technical_score import score_technical
from scoring.apply_boosts import apply_boost
import pandas as pd

def generate_score():
    os.makedirs("daily_scores", exist_ok=True)

    scores = {
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
        "price": score_price(),
        "cot": None,
        "weather": score_weather(),
        "export": score_export(),
        "technical": score_technical()
    }

    cot_score, cot_weighted = score_cot()
    scores["cot"] = cot_score

    base_score = sum(v for v in scores.values() if isinstance(v, (int, float)))
    boosted_score = apply_boost(scores)

    overall = round(boosted_score, 2)

    # Optionally save daily score
    scores["total_score"] = overall
    df = pd.DataFrame([scores])
    df.to_csv(f"daily_scores/{scores['date']}_score.csv", index=False)

    return scores, overall
