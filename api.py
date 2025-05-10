from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generate_score import generate_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later to Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/latest-score")
def get_score():
    scores, total = generate_score()

    return {
        "score": round(total, 2),  # ✅ used by the gauge
        "scores": scores           # ✅ used by the component cards
    }
