from fastapi import FastAPI
from pydantic import BaseModel

from data_loader import DataLoader
from query_engine import QueryEngine
from anomaly_detector import AnomalyDetector


app = FastAPI(
    title="AI Assistant for Ticket Support"
)

# Load CSV

loader = DataLoader(
    "Data_set\\support_tickets.csv"
)

df = loader.load_data()

# Initialize

query_engine = QueryEngine(df)

anomaly_detector = AnomalyDetector(df)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():

    return {
        "message": "AI Assistant for Ticket Support"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer = query_engine.ask(
        request.question
    )

    return {
        "question": request.question,
        "answer": answer
    }


@app.get("/anomalies")
def get_anomalies():

    anomalies = anomaly_detector.detect_anomalies()

    return {
        "count": len(anomalies),
        "anomalies": anomalies
    }