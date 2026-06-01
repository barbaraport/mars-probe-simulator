from app.models.Probe import Probe as ModelProbe
from app.schemas.setup import SetupRequest, SetupResponse
from app.repositories.probe_repository import ProbeRepository
from fastapi import HTTPException


class SetupService:
    def __init__(
        self,
        repository: ProbeRepository,
    ) -> None:
        self.repository = repository

    async def setup(
        self,
        setup: SetupRequest,
    ) -> SetupResponse:
        try:
            probe = await self.repository.setup(
                ModelProbe(x=setup.x, y=setup.y, direction=setup.direction)
            )

            return SetupResponse(
                id=probe.id, x=probe.x, y=probe.y, direction=probe.direction
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail={
                    "code": "SETUP_UNEXPECTED_ERROR",
                    "message": "Unexpected error. Try again in a few seconds.",
                },
            )
