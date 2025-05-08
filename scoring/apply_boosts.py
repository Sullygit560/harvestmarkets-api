# scoring/apply_boosts.py

def apply_boost(scores):
    try:
        # Filter out None values for the base calculation
        valid_scores = {k: v for k, v in scores.items() if isinstance(v, (int, float))}
        base = sum(valid_scores.values()) / len(valid_scores)

        boosted = base

        # Boost logic for bullish signals
        if scores.get("price_score", 0) > 5:
            boosted += 5
        if scores.get("cot_score", 0) > 5:
            boosted += 5
        if scores.get("weather_score", 0) > 70:
            boosted += 10
        if scores.get("export_score", 0) > 5:
            boosted += 5
        if scores.get("technical_score", 0) > 5:
            boosted += 5

        # Bearish boosts (apply subtractive logic if needed)
        if scores.get("cot_score", 0) < -5:
            boosted -= 5
        if scores.get("weather_score", 0) < 30:
            boosted -= 10
        if scores.get("price_score", 0) < -5:
            boosted -= 5

        return round(boosted, 2)

    except Exception as e:
        print(f"❌ Error in boost logic: {e}")
        return sum(v for v in scores.values() if isinstance(v, (int, float)))
