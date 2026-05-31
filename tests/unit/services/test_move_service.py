from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.models.Probe import Probe
from app.schemas.direction import Direction
from app.schemas.move import MoveRequest
from app.services.move_service import MoveService
from fastapi import HTTPException


@pytest.mark.asyncio
async def when_moving_existent_probe_then_should_have_success():
    probe_id = uuid4()

    repo = AsyncMock()
    repo.find_by_id.return_value = Probe(
        id=probe_id, x=0, y=0, direction=Direction.EAST
    )
    repo.save.return_value = Probe(id=probe_id, x=3, y=0, direction=Direction.EAST)

    service = MoveService(repo)

    moved_probe = await service.move(MoveRequest(id=probe_id, command="MMM"))

    repo.create.assert_called_once()
    assert moved_probe.id == probe_id
    assert moved_probe.x == 3
    assert moved_probe.y == 0
    assert moved_probe.direction == Direction.EAST


@pytest.mark.asyncio
async def test_when_moving_nonexistent_probe_then_should_raise_404_error():
    probe_id = uuid4()

    repo = AsyncMock()
    repo.find_by_id.return_value = None

    service = MoveService(repo)

    with pytest.raises(HTTPException) as exc_info:
        await service.move(MoveRequest(id=probe_id, command="MMM"))

    repo.find_by_id.assert_called_once()
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == {
        "code": "PROBE_NOT_FOUND",
        "message": f"Probe {probe_id} not found.",
    }
