import pytest
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.Grid import Grid
from app.models.Probe import Probe
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.direction import Direction


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
    assert probe.grid.y == 5
    assert probe.grid.y == 5


@pytest.mark.asyncio
async def test_when_setup_with_below_0_x_then_db_constraint_should_raise_integrity_error(
    test_session: AsyncSession,
):
    probe = Probe(x=-1, y=0, direction=Direction.WEST)
    test_session.add(probe)

    with pytest.raises(IntegrityError):
        await test_session.commit()

    await test_session.rollback()


@pytest.mark.asyncio
async def test_when_setup_with_below_0_y_then_db_constraint_should_raise_integrity_error(
    test_session: AsyncSession,
):
    probe = Probe(x=0, y=-1, direction=Direction.WEST)
    test_session.add(probe)

    with pytest.raises(IntegrityError):
        await test_session.commit()

    await test_session.rollback()


@pytest.mark.asyncio
async def test_when_setup_with_float_x_then_db_constraint_should_raise_sql_alchemy_error(
    test_session: AsyncSession,
):
    probe = Probe(x=0.6, y=5, direction=Direction.EAST)
    test_session.add(probe)

    with pytest.raises(SQLAlchemyError):
        await test_session.flush()


@pytest.mark.asyncio
async def test_when_setup_with_float_y_then_db_constraint_should_raise_sql_alchemy_error(
    test_session: AsyncSession,
):
    probe = Probe(x=7, y=0.7, direction=Direction.EAST)
    test_session.add(probe)

    with pytest.raises(SQLAlchemyError):
        await test_session.flush()
