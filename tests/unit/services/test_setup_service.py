from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.models.Grid import Grid
from app.models.Probe import Probe
from app.schemas.direction import Direction
from app.schemas.setup import SetupRequest
from app.services.setup_service import SetupService
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_when_creating_valid_probe_and_grid_then_should_have_success():
    repo = AsyncMock()

    probe_id = uuid4()
    grid_id = uuid4()
    repo.setup.return_value = Probe(
        id=probe_id,
        x=0,
        y=0,
        direction=Direction.EAST,
        grid=Grid(id=grid_id, x=20, y=20),
    )

    service = SetupService(repo)

    created_probe = await service.setup(
        SetupRequest(x=20, y=20, direction=Direction.EAST)
    )

    repo.setup.assert_called_once()
    assert created_probe.id == probe_id
    assert created_probe.x == 0
    assert created_probe.y == 0
    assert created_probe.direction == Direction.EAST


@pytest.mark.asyncio
async def test_when_repository_raises_then_service_raises_unexpected_error():
    repo = AsyncMock()
    repo.setup.side_effect = Exception("unexpected failure")

    service = SetupService(repo)

    with pytest.raises(HTTPException) as exc_info:
        await service.setup(SetupRequest(x=20, y=20, direction=Direction.EAST))

    repo.setup.assert_called_once()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == {
        "code": "SETUP_UNEXPECTED_ERROR",
        "message": "Unexpected error. Try again in a few seconds.",
    }
