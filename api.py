from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/latest-score")
def get_score():
    scores = {
        "price": 3.5,
        "cot": 8.61,
        "weather": 50.0,
        "export": 1,
        "technical": 2.8,
        "news": 50
    }

    avg_score = sum(scores.values()) / len(scores)

    return {
        "date": "2025-05-05",  # You can make this dynamic later
        "score": round(avg_score, 2),  # Overall score for the gauge
        "scores": scores  # Individual component scores
    }
