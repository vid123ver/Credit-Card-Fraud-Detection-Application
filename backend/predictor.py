
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "random_forest_v1.pkl"
SCALER_PATH = BASE_DIR / "models" / "model_scaler.pkl"

THRESHOLD = 0.50

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

V_COLUMNS = [f"V{i}" for i in range(1, 29)]

FEATURE_COLUMNS = (
    ["Time"]
    + V_COLUMNS
    + ["Amount"]
    + [
        "Time_hours",
        "Amount_log",
        "V_mean",
        "V_std",
        "V_abs_mean",
        "V_max",
        "V_min",
    ]
)


def predict_transaction(transaction):
    transaction_data = transaction.model_dump(
        exclude={"transaction_id"}
    )

    df = pd.DataFrame([transaction_data])

    df["Time_hours"] = df["Time"] / 3600
    df["Amount_log"] = np.log1p(df["Amount"])

    df["V_mean"] = df[V_COLUMNS].mean(axis=1)
    df["V_std"] = df[V_COLUMNS].std(axis=1)
    df["V_abs_mean"] = df[V_COLUMNS].abs().mean(axis=1)
    df["V_max"] = df[V_COLUMNS].max(axis=1)
    df["V_min"] = df[V_COLUMNS].min(axis=1)

    df = df[FEATURE_COLUMNS]

    scaled_data = scaler.transform(df)

    fraud_probability = float(
        model.predict_proba(scaled_data)[0][1]
    )

    prediction = (
        "Fraud"
        if fraud_probability >= THRESHOLD
        else "Legitimate"
    )

    return {
        "transaction_id": transaction.transaction_id,
        "fraud_probability": round(fraud_probability, 4),
        "fraud_probability_percent": round(
            fraud_probability * 100, 2
        ),
        "prediction": prediction,
        "threshold": THRESHOLD,
        "model": "Random Forest",
        "model_version": "v1",
    }
