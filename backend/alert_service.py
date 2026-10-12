
from datetime import datetime, timezone

from bson import ObjectId
from backend.database import alerts_collection


def create_alert(prediction):
    if prediction["risk_level"] != "High":
        return None

    alert = {
        "transaction_id": prediction["transaction_id"],
        "fraud_probability": prediction["fraud_probability"],
        "prediction": prediction["prediction"],
        "risk_level": prediction["risk_level"],
        "status": "Open",
        "notes": "",
        "created_at": datetime.now(timezone.utc),
    }

    result = alerts_collection.insert_one(alert)

    return {
        "alert_id": str(result.inserted_id),
        "transaction_id": alert["transaction_id"],
        "risk_level": alert["risk_level"],
        "status": alert["status"],
    }


def get_alerts(status=None, limit=100):
    query = {}

    if status is not None:
        query["status"] = status

    alerts = alerts_collection.find(query).sort(
        "created_at", -1
    ).limit(limit)

    results = []

    for alert in alerts:
        results.append({
            "alert_id": str(alert["_id"]),
            "transaction_id": alert["transaction_id"],
            "fraud_probability": alert["fraud_probability"],
            "prediction": alert["prediction"],
            "risk_level": alert["risk_level"],
            "status": alert["status"],
            "notes": alert["notes"],
            "created_at": alert["created_at"].isoformat(),
        })

    return results
