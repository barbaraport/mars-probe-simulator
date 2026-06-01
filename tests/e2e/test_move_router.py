from app.schemas.move import MoveRequest
from app.schemas.setup import Direction, SetupRequest
from tests.utils import is_valid_uuid
from httpx import AsyncClient
from uuid import uuid4
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


@pytest.mark.asyncio
async def test_when_moving_nonexistent_probe_then_response_should_be_404(
    client: AsyncClient,
):
    probe_id = uuid4()
    move_payload = MoveRequest(id=probe_id, command="MRM")
    move_response = await client.patch(
        "/api/v1/move", json=move_payload.model_dump(mode="json")
    )
    data = move_response.json()

    assert move_response.status_code == 404
    assert data["detail"]["code"] == "PROBE_NOT_FOUND"
    assert data["detail"]["message"] == f"Probe {str(probe_id)} not found."


@pytest.mark.asyncio
async def test_when_moving_with_invalid_command_then_response_should_be_400(
    client: AsyncClient,
):
    create_payload = SetupRequest(x=5, y=5, direction=Direction.NORTH)
    create_response = await client.post(
        "/api/v1/setup", json=create_payload.model_dump(mode="json")
    )

    probe_id = create_response.json()["id"]
    move_payload = MoveRequest(id=probe_id, command="MXM")
    move_response = await client.patch(
        "/api/v1/move", json=move_payload.model_dump(mode="json")
    )
    data = move_response.json()

    assert move_response.status_code == 400
    assert data["detail"]["code"] == "INVALID_COMMAND_ERROR"
    assert (
        data["detail"]["message"]
        == "The command 'X' does not exist. The existent commands are: M, L, R. For security, no commands were delivered to the probe."
    )


@pytest.mark.asyncio
async def test_when_moving_beyond_grid_boundaries_then_response_should_be_422(
    client: AsyncClient,
):
    create_payload = SetupRequest(x=3, y=0, direction=Direction.EAST)
    create_response = await client.post(
        "/api/v1/setup", json=create_payload.model_dump(mode="json")
    )

    probe_id = create_response.json()["id"]
    move_payload = MoveRequest(id=probe_id, command="MMMM")
    move_response = await client.patch(
        "/api/v1/move", json=move_payload.model_dump(mode="json")
    )
    data = move_response.json()

    assert move_response.status_code == 422
    assert data["detail"]["code"] == "INVALID_MOVEMENT_ERROR"
    assert (
        data["detail"]["message"]
        == "Movement outside grid limits. The probe must not exceed the grid size of (3, 0). For security, no commands were delivered to the probe."
    )


@pytest.mark.asyncio
async def test_when_moving_with_empty_command_then_should_reject_empty_command_and_raise_422(
    client: AsyncClient,
):
    create_payload = SetupRequest(x=2, y=2, direction=Direction.NORTH)
    create_response = await client.post(
        "/api/v1/setup", json=create_payload.model_dump(mode="json")
    )

    probe_id = create_response.json()["id"]
    move_response = await client.patch(
        "/api/v1/move", json={"id": probe_id, "command": "   "}
    )
    data = move_response.json()

    assert move_response.status_code == 422
    assert data["detail"][0]["loc"] == ["body", "command"]
    assert data["detail"][0]["type"] == "string_too_short"
    assert data["detail"][0]["msg"] == "String should have at least 1 character"
