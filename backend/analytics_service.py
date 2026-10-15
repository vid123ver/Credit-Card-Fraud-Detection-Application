from datetime import datetime, timedelta, timezone

from backend.database import transactions_collection


def get_fraud_analytics():
    total = transactions_collection.count_documents({})

    fraud = transactions_collection.count_documents({
        "prediction": "Fraud"
    })

    legitimate = transactions_collection.count_documents({
        "prediction": "Legitimate"
    })

    risk_pipeline = [
        {
            "$group": {
                "_id": "$risk_level",
                "count": {"$sum": 1},
            }
        }
    ]

    risk_counts = {
        "Low": 0,
        "Medium": 0,
        "High": 0,
    }

    for item in transactions_collection.aggregate(risk_pipeline):
        level = item["_id"]
        if level in risk_counts:
            risk_counts[level] = item["count"]

    cutoff = datetime.now(timezone.utc) - timedelta(days=6)

    trend_pipeline = [
        {
            "$match": {
                "created_at": {"$gte": cutoff}
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$created_at",
                        "timezone": "UTC",
                    }
                },
                "transactions": {"$sum": 1},
                "fraud": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$prediction", "Fraud"]},
                            1,
                            0,
                        ]
                    }
                },
            }
        },
        {"$sort": {"_id": 1}},
    ]

    trend = [
        {
            "date": item["_id"],
            "transactions": item["transactions"],
            "fraud": item["fraud"],
        }
        for item in transactions_collection.aggregate(trend_pipeline)
    ]

    return {
        "total_transactions": total,
        "fraud_detected": fraud,
        "legitimate_transactions": legitimate,
        "fraud_rate_percent": round(
            fraud / total * 100, 2
        ) if total else 0,
        "risk_distribution": risk_counts,
        "daily_trend": trend,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }