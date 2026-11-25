from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_case_uses_shared_contract() -> None:
    payload = {
        "text": "Two cats are gathering near the rubbish chute.",
        "language": "en",
        "photo_urls": [],
        "block": "101",
        "floor": "3",
        "stairwell": "A",
        "zone_id": "zone-demo",
    }
    with TestClient(app) as client:
        response = client.post("/api/v1/cases", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"].startswith("CASE-")
    assert body["status"] == "new"
    assert body["text"] == payload["text"]


def test_mock_detection_never_claims_ai_confidence() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/detect",
            json={"source": "sample.jpg", "reported_species": "cat"},
        )
    assert response.status_code == 202
    body = response.json()
    assert body["confidence"] == 0
    assert body["model_version"] == "mock-starter-no-model"
    assert body["review_status"] == "pending"
