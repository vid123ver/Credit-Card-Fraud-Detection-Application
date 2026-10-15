
from datetime import datetime, timezone

from backend.database import transactions_collection


def save_transaction(transaction, prediction):
    transaction_data = (
        transaction.model_dump()
        if hasattr(transaction, "model_dump")
        else dict(transaction)
    )

    record = {
        **transaction_data,
        **prediction,
        "created_at": datetime.now(timezone.utc),
    }

    transactions_collection.insert_one(record)

    return {
        "transaction_id": prediction["transaction_id"],
        "saved": True,
    }


def get_transactions(limit=100):
    records = transactions_collection.find().sort(
        "created_at", -1
    ).limit(limit)

    results = []

    for record in records:
        record["_id"] = str(record["_id"])
        if "created_at" in record:
            record["created_at"] = record["created_at"].isoformat()
        results.append(record)

    return results
