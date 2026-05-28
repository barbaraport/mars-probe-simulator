from fastapi.testclient import TestClient
from app.main import app
from app.schemas.setup import Direction, SetupRequest
from tests.utils import is_valid_uuid

client = TestClient(app)


def test_example_response():
    payload = SetupRequest(x=5, y=5, direction=Direction.NORTH)

    response = client.post("/api/v1/setup", json=payload.model_dump())

    assert response.status_code == 200

    data = response.json()
    assert is_valid_uuid(data["id"])
    assert data["x"] == 0
    assert data["y"] == 0
    assert data["direction"] == "NORTH"
