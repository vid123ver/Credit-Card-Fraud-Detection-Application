from fastapi import FastAPI
from backend.database import test_database_connection
from backend.schemas import TransactionInput

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

@app.post("/transactions/test")
def test_transaction(transaction: TransactionInput):
    return {
        "message": "Transaction data is valid",
        "transaction_id": transaction.transaction_id,
        "amount": transaction.Amount
    }