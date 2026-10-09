
from fastapi import FastAPI

from backend.database import test_database_connection
from backend.schemas import TransactionInput
from backend.predictor import predict_transaction
from backend.batch_schemas import BatchPredictionInput
from backend.predictor import predict_transactions
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
    try:
        test_database_connection()
        database_status = "connected"
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


@app.post("/predict")
def predict(transaction: TransactionInput):
    return predict_transaction(transaction)


@app.post("/predict/batch")
def predict_batch(batch: BatchPredictionInput):
    predictions = predict_transactions(batch.transactions)

    return {
        "total_transactions": len(predictions),
        "predictions": predictions
    }