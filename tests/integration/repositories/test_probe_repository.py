import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.Grid import Grid
from app.models.Probe import Probe
from app.repositories.probe_repository import ProbeRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.direction import Direction


################################################################################
# Constraint tests
################################################################################


@pytest.mark.asyncio
async def test_when_setup_valid_probe_and_grid_then_should_create_successfully(
    test_session: AsyncSession,
):
    probe = Probe(x=0, y=0, direction=Direction.WEST, grid=Grid(x=5, y=5))
    test_session.add(probe)
    await test_session.flush()
    await test_session.refresh(probe, attribute_names=["grid"])

    assert probe.id is not None
    assert probe.x == 0
    assert probe.y == 0
    assert probe.direction == Direction.WEST
    assert probe.grid.id is not None
    assert probe.grid.x == 5
    assert probe.grid.y == 5


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("x", "y", "direction"),
    [
        (-1, 0, Direction.WEST),
        (0, -1, Direction.WEST),
        (0, 0, None),
    ],
)
async def test_when_setup_with_invalid_probe_then_should_raise_integrity_error(
    test_session: AsyncSession,
    x: int,
    y: int,
    direction: Direction,
):
    probe = Probe(x=x, y=y, direction=direction)
    test_session.add(probe)

    with pytest.raises(IntegrityError):
        await test_session.commit()

    await test_session.rollback()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("x", "y"),
    [
        (-1, 0),
        (0, -1),
    ],
)
async def test_when_setup_with_invalid_grid_then_should_raise_integrity_error(
    test_session: AsyncSession,
    x: int,
    y: int,
):
    probe = Probe(x=0, y=0, direction=Direction.NORTH, grid=Grid(x=x, y=y))
    test_session.add(probe)

    with pytest.raises(IntegrityError):
        await test_session.commit()

    await test_session.rollback()


# Updating section
@pytest.mark.asyncio
async def test_when_update_with_below_0_y_then_db_constraint_should_raise_integrity_error(
    test_session: AsyncSession,
):
    probe = Probe(x=2, y=2, direction=Direction.SOUTH, grid=Grid(x=2, y=2))
    test_session.add(probe)
    await test_session.commit()
    await test_session.refresh(probe)

    probe.y = -1

    with pytest.raises(IntegrityError):
        await test_session.flush()

    await test_session.rollback()


################################################################################
# Repository tests
################################################################################


@pytest.mark.asyncio
async def test_when_save_probe_then_should_merge_and_return_saved_probe(
    test_session: AsyncSession,
):
    repository = ProbeRepository(test_session)
    probe = Probe(x=1, y=1, direction=Direction.EAST, grid=Grid(x=5, y=5))

    saved_probe = await repository.save(probe)

    assert saved_probe.id is not None
    assert saved_probe.x == 1
    assert saved_probe.y == 1
    assert saved_probe.direction == Direction.EAST
    assert saved_probe.grid is not None
    assert saved_probe.grid.id is not None
    assert saved_probe.grid.x == 5
    assert saved_probe.grid.y == 5


@pytest.mark.asyncio
async def test_when_find_probe_by_id_then_should_return_probe(
    test_session: AsyncSession,
):
    repository = ProbeRepository(test_session)
    probe = Probe(x=3, y=3, direction=Direction.NORTH, grid=Grid(x=3, y=3))
    saved_probe = await repository.save(probe)

    found_probe = await repository.find_by_id(saved_probe.id)

    assert found_probe is not None
    assert found_probe.id == saved_probe.id
    assert found_probe.x == 3
    assert found_probe.y == 3


@pytest.mark.asyncio
async def test_when_find_all_then_should_return_saved_probes(
    test_session: AsyncSession,
):
    repository = ProbeRepository(test_session)
    first_probe = Probe(x=4, y=4, direction=Direction.EAST, grid=Grid(x=4, y=4))
    second_probe = Probe(x=5, y=5, direction=Direction.SOUTH, grid=Grid(x=5, y=5))

    await repository.save(first_probe)
    await repository.save(second_probe)

    all_probes = await repository.find_all()

    assert len(all_probes) == 2
    assert {probe.x for probe in all_probes} == {4, 5}
    assert {probe.y for probe in all_probes} == {4, 5}


@pytest.mark.asyncio
async def test_when_setup_repository_then_should_create_probe_and_grid(
    test_session: AsyncSession,
):
    repository = ProbeRepository(test_session)
    probe = Probe(x=5, y=5, direction=Direction.SOUTH)

    saved_probe = await repository.setup(probe)

    assert saved_probe.id is not None
    assert saved_probe.x == 0
    assert saved_probe.y == 0
    assert saved_probe.direction == Direction.SOUTH
    assert saved_probe.grid is not None
    assert saved_probe.grid.x == 5
    assert saved_probe.grid.y == 5


@pytest.mark.asyncio
async def test_when_find_by_id_with_missing_probe_then_should_return_none(
    test_session: AsyncSession,
):
    repository = ProbeRepository(test_session)
    missing_id = uuid.uuid4()

    found_probe = await repository.find_by_id(missing_id)

    assert found_probe is None
