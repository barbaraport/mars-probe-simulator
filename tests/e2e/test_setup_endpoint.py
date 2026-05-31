from app.schemas.setup import Direction, SetupRequest
from tests.utils import is_valid_uuid
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_when_creating_valid_setup_then_response_should_be_200(
    client: AsyncClient,
):
    payload = SetupRequest(x=5, y=5, direction=Direction.NORTH)

    response = await client.post("/api/v1/setup", json=payload.model_dump(mode="json"))

    assert response.status_code == 200

    data = response.json()
    assert is_valid_uuid(data["id"])
    assert data["x"] == 0
    assert data["y"] == 0
    assert data["direction"] == "NORTH"
