from app.schemas.check import CheckResponse
from app.repositories.probe_repository import ProbeRepository
from app.schemas.probe import ProbeResponse


class CheckService:
    def __init__(
        self,
        repository: ProbeRepository,
    ) -> None:
        self.repository = repository

    async def check(
        self,
    ) -> CheckResponse:
        probes = [
            ProbeResponse(id=probe.id, x=probe.x, y=probe.y, direction=probe.direction)
            for probe in await self.repository.find_all()
        ]
        return CheckResponse(probes=list(probes))
