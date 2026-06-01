from app.schemas.setup import Direction, SetupRequest
from httpx import AsyncClient
import pytest

from tests.utils import is_valid_uuid


@pytest.mark.asyncio
async def test_when_setting_up_one_probe_should_return_one_probe(client: AsyncClient):
    create_payload = SetupRequest(x=5, y=5, direction=Direction.NORTH)
    await client.post("/api/v1/setup", json=create_payload.model_dump(mode="json"))

    check_response = await client.get("/api/v1/check")
    data = check_response.json()

    assert len(data["probes"]) == 1
    assert is_valid_uuid(data["probes"][0]["id"])
    assert data["probes"][0]["x"] == 0
    assert data["probes"][0]["y"] == 0


@pytest.mark.asyncio
async def test_when_setting_up_multiple_probes_should_return_all_probes(
    client: AsyncClient,
):
    payloads = [
        SetupRequest(x=1, y=1, direction=Direction.EAST),
        SetupRequest(x=2, y=3, direction=Direction.SOUTH),
    ]

    for p in payloads:
        await client.post("/api/v1/setup", json=p.model_dump(mode="json"))

    check_response = await client.get("/api/v1/check")
    data = check_response.json()

    assert len(data["probes"]) == len(payloads)
    assert is_valid_uuid(data["probes"][0]["id"])
    assert data["probes"][0]["x"] == 0
    assert data["probes"][0]["y"] == 0
    assert is_valid_uuid(data["probes"][1]["id"])
    assert data["probes"][1]["x"] == 0
    assert data["probes"][1]["y"] == 0


@pytest.mark.asyncio
async def test_when_no_probes_should_return_empty_list(client: AsyncClient):
    check_response = await client.get("/api/v1/check")
    data = check_response.json()

    assert isinstance(data.get("probes"), list)
    assert len(data["probes"]) == 0
