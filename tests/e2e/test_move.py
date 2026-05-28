from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_example_response():
    payload = {"command": "MRM"}

    response = client.post("/api/v1/move", json=payload)

    assert response.status_code == 200
    assert response.json() == {"id": "abc123", "x": 1, "y": 1, "direction": "EAST"}
