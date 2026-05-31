from app.schemas.move import MoveRequest
from app.schemas.setup import Direction, SetupRequest
from tests.utils import is_valid_uuid
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_when_moving_to_valid_coordinates_then_response_should_be_200(
    client: AsyncClient,
):
    create_payload = SetupRequest(x=5, y=5, direction=Direction.NORTH)
    create_response = await client.post(
        "/api/v1/setup", json=create_payload.model_dump(mode="json")
    )

    probe_id = create_response.json()["id"]

    assert is_valid_uuid(probe_id)

    move_payload = MoveRequest(id=probe_id, command="MRM")
    move_response = await client.patch(
        "/api/v1/move", json=move_payload.model_dump(mode="json")
    )
    data = move_response.json()

    assert data["id"] == probe_id
    assert data["x"] == 1
    assert data["y"] == 1
    assert data["direction"] == "EAST"
