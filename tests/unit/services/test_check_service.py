from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.models.Probe import Probe
from app.schemas.direction import Direction
from app.services.check import CheckService


@pytest.mark.asyncio
async def test_when_fetching_5_probes_then_should_have_list_with_5_probes():
    repo = AsyncMock()
    repo.find_all.return_value = [
        Probe(id=uuid4(), x=1, y=1, direction=Direction.NORTH),
        Probe(id=uuid4(), x=2, y=2, direction=Direction.NORTH),
        Probe(id=uuid4(), x=3, y=3, direction=Direction.NORTH),
        Probe(id=uuid4(), x=4, y=4, direction=Direction.NORTH),
        Probe(id=uuid4(), x=5, y=5, direction=Direction.NORTH),
    ]

    service = CheckService(repo)
    probes_list = await service.check()

    assert len(probes_list.probes) == 5


@pytest.mark.asyncio
async def test_when_fetching_no_probes_then_should_receive_empty_list():
    repo = AsyncMock()
    repo.find_all.return_value = []

    service = CheckService(repo)
    probes_list = await service.check()

    assert len(probes_list.probes) == 0
