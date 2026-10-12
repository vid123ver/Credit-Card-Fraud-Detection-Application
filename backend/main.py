
from fastapi import FastAPI, Query

from backend.database import test_database_connection
from backend.schemas import TransactionInput
from backend.batch_schemas import BatchPredictionInput
from backend.predictor import (
    predict_transaction,
    predict_transactions,
    DEFAULT_THRESHOLD,
)
from backend.alert_service import create_alert, get_alerts

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
def predict(
    transaction: TransactionInput,
    threshold: float = Query(
        default=DEFAULT_THRESHOLD,
        ge=0.0,
        le=1.0
    )
):
    result = predict_transaction(transaction, threshold)

    alert = create_alert(result)
    result["alert"] = alert

    return result


@app.post("/predict/batch")
def predict_batch(
    batch: BatchPredictionInput,
    threshold: float = Query(
        default=DEFAULT_THRESHOLD,
        ge=0.0,
        le=1.0
    )
):
    predictions = predict_transactions(
        batch.transactions,
        threshold
    )

    for prediction in predictions:
        prediction["alert"] = create_alert(prediction)

    return {
        "total_transactions": len(predictions),
        "threshold": threshold,
        "predictions": predictions
    }


@app.get("/alerts")
def list_alerts(
    status: str | None = Query(
        default=None,
        pattern="^(Open|Reviewed|Resolved)$"
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=500
    )
):
    alerts = get_alerts(status=status, limit=limit)

    return {
        "total_alerts": len(alerts),
        "alerts": alerts
    }