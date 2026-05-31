from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.models.Grid import Grid
from app.models.Probe import Probe
from app.schemas.direction import Direction
from app.schemas.setup import SetupRequest
from app.services.setup import SetupService


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

    created_probe = await service.process(
        SetupRequest(x=20, y=20, direction=Direction.EAST)
    )

    repo.setup.assert_called_once()
    assert created_probe.id == probe_id
    assert created_probe.x == 0
    assert created_probe.y == 0
    assert created_probe.direction == Direction.EAST
