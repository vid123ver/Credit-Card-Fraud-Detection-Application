from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.analytics_service import get_fraud_analytics
from backend.model_service import (
    get_model_performance,
    get_model_metadata,
)
from backend.database import test_database_connection
from backend.schemas import TransactionInput
from backend.batch_schemas import BatchPredictionInput
from backend.predictor import (
    predict_transaction,
    predict_transactions,
    DEFAULT_THRESHOLD,
)
from backend.alert_service import create_alert, get_alerts
from backend.transaction_service import (
    save_transaction,
    get_transactions,
)


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="AI-Powered Credit Card Fraud Detection API",
    version="1.0.0",
    description="API for credit card fraud detection and alert management.",
)


# --------------------------------------------------
# CORS Middleware
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Credit Card Fraud Detection API is running",
        "status": "success",
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():
    try:
        test_database_connection()
        database_status = "connected"
    except Exception:
        database_status = "disconnected"

    return {
        "status": "healthy",
        "database": database_status,
    }


# --------------------------------------------------
# Transaction Input Validation
# --------------------------------------------------

@app.post("/transactions/test")
def test_transaction(transaction: TransactionInput):
    return {
        "message": "Transaction data is valid",
        "transaction_id": transaction.transaction_id,
        "amount": transaction.Amount,
    }


# --------------------------------------------------
# Get Stored Transactions
# --------------------------------------------------

@app.get("/transactions")
def list_transactions(
    limit: int = Query(default=100, ge=1, le=500),
):
    try:
        transactions = get_transactions(limit=limit)

        return {
            "total_transactions": len(transactions),
            "transactions": transactions,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve transactions.",
        ) from error


# --------------------------------------------------
# Single Transaction Fraud Prediction
# --------------------------------------------------

@app.post("/predict")
def predict(
    transaction: TransactionInput,
    threshold: float = Query(
        default=DEFAULT_THRESHOLD,
        ge=0.0,
        le=1.0,
    ),
):
    try:
        result = predict_transaction(transaction, threshold)

        # Save transaction and prediction to MongoDB.
        save_transaction(transaction, result)

        # Create an alert when applicable.
        result["alert"] = create_alert(result)

        return result

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Transaction prediction failed.",
        ) from error


# --------------------------------------------------
# Batch Transaction Fraud Prediction
# --------------------------------------------------

@app.post("/predict/batch")
def predict_batch(
    batch: BatchPredictionInput,
    threshold: float = Query(
        default=DEFAULT_THRESHOLD,
        ge=0.0,
        le=1.0,
    ),
):
    try:
        predictions = predict_transactions(
            batch.transactions,
            threshold,
        )

        for transaction, prediction in zip(
            batch.transactions,
            predictions,
        ):
            # Save each transaction and its prediction.
            save_transaction(transaction, prediction)

            # Create an alert when applicable.
            prediction["alert"] = create_alert(prediction)

        return {
            "total_transactions": len(predictions),
            "threshold": threshold,
            "predictions": predictions,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Batch prediction failed.",
        ) from error


# --------------------------------------------------
# Alert Management
# --------------------------------------------------

@app.get("/alerts")
def list_alerts(
    status: str | None = Query(
        default=None,
        pattern="^(Open|Reviewed|Resolved)$",
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
):
    try:
        alerts = get_alerts(
            status=status,
            limit=limit,
        )

        return {
            "total_alerts": len(alerts),
            "alerts": alerts,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve alerts.",
        ) from error


# --------------------------------------------------
# Model Performance API
# --------------------------------------------------

@app.get("/models/performance")
def model_performance():
    try:
        return get_model_performance()

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve model performance.",
        ) from error


# --------------------------------------------------
# Model Metadata API
# --------------------------------------------------

@app.get("/models/metadata")
def model_metadata():
    try:
        return get_model_metadata()

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve model metadata.",
        ) from error


@app.get("/analytics/fraud")
def fraud_analytics():
    try:
        return get_fraud_analytics()
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve fraud analytics.",
        ) from error
