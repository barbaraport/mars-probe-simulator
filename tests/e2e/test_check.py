from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_example_response():
    response = client.get("/api/v1/move")

    assert response.status_code == 200
    assert response.json() == {
        "probes": [
            {"id": "abc123", "x": 1, "y": 1, "direction": "EAST"},
            {"id": "xyzbas1234", "x": 3, "y": 4, "direction": "NORTH"},
        ]
    }
