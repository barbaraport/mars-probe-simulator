from unittest.mock import AsyncMock
from uuid import uuid4
import pytest

from app.models.Probe import Probe
from app.schemas.direction import Direction
from app.services.check_service import CheckService
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_when_fetching_3_probes_then_should_have_list_with_3_probes():
    repo = AsyncMock()
    probes = [
        Probe(id=uuid4(), x=0, y=0, direction=Direction.NORTH),
        Probe(id=uuid4(), x=256, y=128, direction=Direction.EAST),
        Probe(id=uuid4(), x=999999, y=999999, direction=Direction.SOUTH),
    ]

    repo.find_all.return_value = probes

    service = CheckService(repo)
    probes_list = await service.check()

    assert len(probes_list.probes) == len(probes)
    for original, returned in zip(probes, probes_list.probes):
        assert returned.id == original.id
        assert returned.x == original.x
        assert returned.y == original.y
        assert returned.direction == original.direction


@pytest.mark.asyncio
async def test_when_fetching_no_probes_then_should_receive_empty_list():
    repo = AsyncMock()
    repo.find_all.return_value = []

    service = CheckService(repo)
    probes_list = await service.check()

    assert len(probes_list.probes) == 0


@pytest.mark.asyncio
async def test_when_repository_raises_then_service_raises_exception():
    repo = AsyncMock()
    repo.find_all.side_effect = HTTPException(
        status_code=500, detail="unexpected error"
    )

    service = CheckService(repo)

    with pytest.raises(HTTPException) as exc_info:
        await service.check()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == {
        "code": "CHECK_UNEXPECTED_ERROR",
        "message": "Unexpected error. Try again in a few seconds.",
    }
