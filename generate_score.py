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

# Create output directory
os.makedirs("daily_scores", exist_ok=True)

# Fetch component scores
scores = {
    "date": datetime.now(UTC).strftime("%Y-%m-%d"),
    "price_score": score_price(),
    "cot_score": None,
    "weather_score": score_weather(),
    "export_score": score_export(),
    "technical_score": score_technical()
}

# Fetch COT score separately (returns tuple)
cot_score, cot_weighted = score_cot()
scores["cot_score"] = cot_score
scores["cot_weighted"] = cot_weighted

# Compute total score from available components (ignores None)
base_score = sum(v for k, v in scores.items() if isinstance(v, (int, float)) and "_score" in k) / 5
boosted_score = apply_boost(scores)

scores["total_score"] = round(boosted_score, 2)

# Save daily score
df = pd.DataFrame([scores])
output_path = f"daily_scores/{scores['date']}_score.csv"
df.to_csv(output_path, index=False)

print("✅ Score written:", scores)
