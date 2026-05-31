from app.schemas.setup import Direction, SetupRequest
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_when_setting_up_one_probe_should_return_one_probe(client: AsyncClient):
    create_payload = SetupRequest(x=5, y=5, direction=Direction.NORTH)
    await client.post("/api/v1/setup", json=create_payload.model_dump(mode="json"))

    check_response = await client.get("/api/v1/check")
    data = check_response.json()

    assert len(data["probes"]) == 1
