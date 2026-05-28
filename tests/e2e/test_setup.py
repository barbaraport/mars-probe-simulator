from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_example_response():
    payload = {"x": 5, "y": 5, "direction": "NORTH"}

    response = client.post("/api/v1/setup", json=payload)

    assert response.status_code == 200
    assert response.json() == {"id": "abc123", "x": 0, "y": 0, "direction": "NORTH"}
