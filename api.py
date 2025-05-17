from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generate_score import generate_score

import os
import json
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LAST_SCORE_FILE = "last_score.json"

def send_alert_email(old_score, new_score, recommendation):
    sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    from_email = os.getenv("ALERT_EMAIL_FROM")
    to_email = os.getenv("ALERT_EMAIL_TO")

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    subject = f"📊 Sentiment Score Updated: {new_score}"
    content = f"""
Sentiment Score Update

Timestamp: {timestamp}
Old Score: {old_score}
New Score: {new_score}
Recommendation: {recommendation}

Visit your dashboard for details.
"""

    message = Mail(from_email=from_email, to_emails=to_email, subject=subject, plain_text_content=content)
    response = sg.send(message)
    print(f"[SendGrid] Email sent — Status: {response.status_code}")
    return response.status_code

def get_last_score():
    if os.path.exists(LAST_SCORE_FILE):
        with open(LAST_SCORE_FILE, "r") as f:
            return json.load(f).get("score")
    return None

def store_latest_score(score):
    with open(LAST_SCORE_FILE, "w") as f:
        json.dump({"score": score}, f)

def get_recommendation(score):
    if score >= 66:
        return "Bullish — Consider Long"
    elif score <= 33:
        return "Bearish — Consider Short"
    return "Neutral — Hold/Wait"

def check_and_notify_score(score):
    old_score = get_last_score()
    print(f"[DEBUG] Old score: {old_score}, New score: {score}")
    if True:  # Force alert temporarily
        recommendation = get_recommendation(score)
        print("[DEBUG] Triggering SendGrid email...")
        send_alert_email(old_score, score, recommendation)
        store_latest_score(score)

@app.get("/api/latest-score")
def get_score():
    scores, total = generate_score()
    rounded_score = round(total, 2)

    check_and_notify_score(rounded_score)  # ✅ This MUST be here!

    return {
        "score": rounded_score,
        "scores": scores
    }

