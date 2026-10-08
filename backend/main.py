from fastapi import FastAPI
from backend.database import test_database_connection

app = FastAPI(
    title="AI-Powered Credit Card Fraud Detection API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Credit Card Fraud Detection API is running"
    }


@app.get("/health")
def health():
    database_status = "connected"

    try:
        test_database_connection()
    except Exception:
        database_status = "disconnected"

    return {
        "status": "healthy",
        "database": database_status
    }