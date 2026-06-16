from fastapi import FastAPI
from pydantic import BaseModel

from query_engine import answer_question
from anomaly_detection import detect_anomalies

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "message": "Support Ticket Analytics API"
    }

@app.post("/ask")
def ask(q: Question):

    return {
        "question": q.question,
        "answer": answer_question(
            q.question
        )
    }

@app.get("/anomalies")
def anomalies():

    try:
        return detect_anomalies()

    except Exception as e:
        return {
            "error": str(e)
        }