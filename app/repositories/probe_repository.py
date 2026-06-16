from typing import Sequence
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.logging import Logger
from app.models.Grid import Grid
from app.models.Probe import Probe


class ProbeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_ready(self) -> bool:
        try:
            await self.session.execute(select(1))
            return True
        except Exception as e:
            Logger.error(f"Database readiness check failed: {e}", exc_info=True)
            return False

    async def setup(
        self,
        position: Probe,
    ) -> Probe:
        probe = Probe(x=0, y=0, direction=position.direction)
        grid = Grid(x=position.x, y=position.y)
        probe.grid = grid

        self.session.add(probe)

        await self.session.commit()
        await self.session.refresh(probe)

        return probe

    async def save(self, probe: Probe) -> Probe:
        merged = await self.session.merge(probe)
        await self.session.commit()
        await self.session.refresh(merged)

        return merged

    async def find_by_id(self, id: UUID) -> Probe | None:
        statement = (
            select(Probe).options(selectinload(Probe.grid)).where(Probe.id == id)
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def find_all(self) -> Sequence[Probe]:
        probes = await self.session.scalars(select(Probe))
        return probes.all()
