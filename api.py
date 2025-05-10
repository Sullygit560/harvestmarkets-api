from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generate_score import generate_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/latest-score")
def get_score():
    scores = generate_score()  # ✅ uses real scores

    avg_score = sum(scores.values()) / len(scores)

    return {
        "score": round(avg_score, 2),  # For the gauge
        "scores": scores               # For component cards
    }
