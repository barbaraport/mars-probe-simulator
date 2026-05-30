from app.schemas.setup import SetupRequest, SetupResponse
from app.repositories.probe import ProbeRepository


class SetupService:
    def __init__(
        self,
        repository: ProbeRepository,
    ) -> None:
        self.repository = repository

    async def process(
        self,
        setup: SetupRequest,
    ) -> SetupResponse:
        probe = await self.repository.setup(setup)

        return SetupResponse(
            id=probe.id, x=probe.x, y=probe.y, direction=probe.direction
        )
