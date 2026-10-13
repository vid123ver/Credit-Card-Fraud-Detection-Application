
from fastapi.testclient import TestClient
import backend.main as main

client = TestClient(main.app)


def valid_transaction():
    transaction = {
        "transaction_id": "TEST-TXN-001",
        "Time": 1000,
        "Amount": 150.0,
    }
    transaction.update({
        f"V{i}": 0.1 for i in range(1, 29)
    })
    return transaction


def sample_prediction(transaction_id="TEST-TXN-001"):
    return {
        "transaction_id": transaction_id,
        "fraud_probability": 0.95,
        "fraud_probability_percent": 95.0,
        "prediction": "Fraud",
        "risk_level": "High",
        "threshold": 0.5,
        "model": "Random Forest",
        "model_version": "v1",
    }


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    main.test_database_connection = lambda: True

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["database"] == "connected"


def test_transaction_validation():
    response = client.post(
        "/transactions/test",
        json=valid_transaction()
    )

    assert response.status_code == 200
    assert response.json()["transaction_id"] == "TEST-TXN-001"


def test_invalid_transaction():
    transaction = valid_transaction()
    transaction["Amount"] = -10

    response = client.post(
        "/transactions/test",
        json=transaction
    )

    assert response.status_code == 422


def test_prediction(monkeypatch):
    monkeypatch.setattr(
        main,
        "predict_transaction",
        lambda transaction, threshold: sample_prediction(
            transaction.transaction_id
        )
    )
    monkeypatch.setattr(
        main,
        "create_alert",
        lambda prediction: {
            "alert_id": "mock-alert-001",
            "status": "Open"
        }
    )
    monkeypatch.setattr(
        main,
        "save_transaction",
        lambda transaction, prediction: None
    )

    response = client.post(
        "/predict",
        json=valid_transaction()
    )

    assert response.status_code == 200
    assert response.json()["prediction"] == "Fraud"
    assert response.json()["alert"]["status"] == "Open"


def test_alert_listing(monkeypatch):
    monkeypatch.setattr(
        main,
        "get_alerts",
        lambda status=None, limit=100: [
            {
                "alert_id": "mock-alert-001",
                "transaction_id": "TEST-TXN-001",
                "risk_level": "High",
                "status": "Open"
            }
        ]
    )

    response = client.get("/alerts?status=Open")

    assert response.status_code == 200
    assert response.json()["total_alerts"] == 1


def test_model_performance(monkeypatch):
    monkeypatch.setattr(
        main,
        "get_model_performance",
        lambda: {
            "total_models": 2,
            "models": []
        }
    )

    response = client.get("/models/performance")

    assert response.status_code == 200
    assert response.json()["total_models"] == 2


def test_model_metadata(monkeypatch):
    monkeypatch.setattr(
        main,
        "get_model_metadata",
        lambda: {
            "model_name": "Random Forest",
            "version": "v1"
        }
    )

    response = client.get("/models/metadata")

    assert response.status_code == 200
    assert response.json()["version"] == "v1"
