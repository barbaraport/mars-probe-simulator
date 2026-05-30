from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.Grid import Grid
from app.models.Probe import Probe
from app.schemas.setup import SetupRequest


class ProbeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def setup(
        self,
        position: SetupRequest,
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
