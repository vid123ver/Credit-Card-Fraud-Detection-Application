
from datetime import datetime, timezone

from bson import ObjectId
from backend.database import alerts_collection


REVIEW_STATUSES = {
    "Open",
    "Under Review",
    "Confirmed Fraud",
    "False Positive",
}


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
            "notes": alert.get("notes", ""),
            "created_at": alert["created_at"].isoformat(),
            "reviewed_at": (
                alert["reviewed_at"].isoformat()
                if alert.get("reviewed_at")
                else None
            ),
        })

    return results


def update_alert_review(alert_id, status, notes=""):
    if status not in REVIEW_STATUSES:
        raise ValueError(
            f"Invalid status. Choose one of: {', '.join(sorted(REVIEW_STATUSES))}"
        )

    if not ObjectId.is_valid(alert_id):
        return None

    reviewed_at = datetime.now(timezone.utc)

    result = alerts_collection.update_one(
        {"_id": ObjectId(alert_id)},
        {
            "$set": {
                "status": status,
                "notes": notes.strip(),
                "reviewed_at": reviewed_at,
            }
        },
    )

    if result.matched_count == 0:
        return None

    return {
        "alert_id": alert_id,
        "status": status,
        "notes": notes.strip(),
        "reviewed_at": reviewed_at.isoformat(),
    }
