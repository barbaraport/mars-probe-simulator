from unittest.mock import AsyncMock, patch
from uuid import UUID, uuid4

import pytest

from app.models.Grid import Grid
from app.models.Probe import Probe
from app.schemas.direction import Direction
from app.schemas.move import MoveRequest
from app.services.move_service import MoveService
from fastapi import HTTPException


def create_probe_with_grid(
    probe_id: UUID | None,
    x: int = 0,
    y: int = 0,
    direction: Direction = Direction.EAST,
    grid_x: int = 3,
    grid_y: int = 3,
) -> Probe:
    if probe_id is None:
        probe_id = uuid4()

    probe = Probe(id=probe_id, x=x, y=y, direction=direction)
    probe.grid = Grid(id=uuid4(), x=grid_x, y=grid_y)

    return probe


@pytest.mark.asyncio
async def test_when_moving_existent_probe_then_should_have_success():
    probe_id = uuid4()
    probe = create_probe_with_grid(probe_id=probe_id)

    repo = AsyncMock()
    repo.find_by_id.return_value = probe
    repo.save.return_value = Probe(id=probe_id, x=3, y=0, direction=Direction.EAST)

    service = MoveService(repo)
    moved_probe = await service.move(MoveRequest(id=probe_id, command="MMM"))

    repo.find_by_id.assert_called_once_with(probe_id)
    repo.save.assert_called_once()

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

    repo.find_by_id.assert_called_once_with(probe_id)
    repo.save.assert_not_called()

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == {
        "code": "PROBE_NOT_FOUND",
        "message": f"Probe {probe_id} not found.",
    }


@pytest.mark.asyncio
async def test_when_moving_with_invalid_command_then_should_raise_400_error():
    probe_id = uuid4()
    probe = create_probe_with_grid(probe_id=probe_id)

    repo = AsyncMock()
    repo.find_by_id.return_value = probe

    service = MoveService(repo)

    with pytest.raises(HTTPException) as exc_info:
        await service.move(MoveRequest(id=probe_id, command="MXM"))

    repo.find_by_id.assert_called_once_with(probe_id)
    repo.save.assert_not_called()

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == {
        "code": "INVALID_COMMAND_ERROR",
        "message": "The command 'X' does not exist. The existent commands are: M, L, R. For security, no commands were delivered to the probe.",
    }


@pytest.mark.asyncio
async def test_when_moving_beyond_grid_limits_then_should_raise_422_error():
    probe_id = uuid4()
    probe = create_probe_with_grid(probe_id=probe_id, x=3, y=0)

    repo = AsyncMock()
    repo.find_by_id.return_value = probe
    repo.save.return_value = Probe(id=probe_id, x=3, y=0, direction=Direction.EAST)

    service = MoveService(repo)

    with pytest.raises(HTTPException) as exc_info:
        await service.move(MoveRequest(id=probe_id, command="M"))

    repo.find_by_id.assert_called_once_with(probe_id)
    repo.save.assert_not_called()

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == {
        "code": "INVALID_MOVEMENT_ERROR",
        "message": "Movement outside grid limits. The probe must not exceed the grid size of (3, 3). For security, no commands were delivered to the probe.",
    }


@pytest.mark.asyncio
async def test_when_command_runner_raises_unexpected_exception_then_should_raise_500_error():
    probe_id = uuid4()
    probe = create_probe_with_grid(probe_id=probe_id)

    repo = AsyncMock()
    repo.find_by_id.return_value = probe

    service = MoveService(repo)

    with patch(
        "app.services.move_service.CommandRunner.run",
        side_effect=Exception("unexpected failure"),
    ):
        with pytest.raises(HTTPException) as exc_info:
            await service.move(MoveRequest(id=probe_id, command="MMM"))

    repo.find_by_id.assert_called_once_with(probe_id)
    repo.save.assert_not_called()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == {
        "code": "MOVE_UNEXPECTED_ERROR",
        "message": "Unexpected error. Try again. For security, no commands were delivered to the probe.",
    }
