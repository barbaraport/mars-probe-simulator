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


@pytest.mark.asyncio
async def test_when_creating_setup_with_x_negative_grid_size_then_response_should_be_422(
    client: AsyncClient,
):
    response = await client.post(
        "/api/v1/setup", json={"x": -1, "y": 5, "direction": "NORTH"}
    )
    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["loc"] == ["body", "x"]
    assert data["detail"][0]["type"] == "greater_than_equal"
    assert data["detail"][0]["msg"] == "Input should be greater than or equal to 0"


@pytest.mark.asyncio
async def test_when_creating_setup_with_y_negative_grid_size_then_response_should_be_422(
    client: AsyncClient,
):
    response = await client.post(
        "/api/v1/setup", json={"x": 5, "y": -2, "direction": "NORTH"}
    )
    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["loc"] == ["body", "y"]
    assert data["detail"][0]["type"] == "greater_than_equal"
    assert data["detail"][0]["msg"] == "Input should be greater than or equal to 0"


@pytest.mark.asyncio
async def test_when_creating_setup_with_invalid_direction_then_response_should_be_422(
    client: AsyncClient,
):
    response = await client.post(
        "/api/v1/setup", json={"x": 5, "y": 5, "direction": "NORTHEAST"}
    )
    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["loc"] == ["body", "direction"]
    assert data["detail"][0]["type"] == "enum"
    assert (
        data["detail"][0]["msg"] == "Input should be 'NORTH', 'SOUTH', 'EAST' or 'WEST'"
    )
