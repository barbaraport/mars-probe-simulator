from app.schemas.check import CheckResponse
from app.repositories.probe_repository import ProbeRepository
from app.schemas.probe import ProbeResponse
from fastapi import HTTPException


class CheckService:
    def __init__(
        self,
        repository: ProbeRepository,
    ) -> None:
        self.repository = repository

    async def process(
        self,
    ) -> CheckResponse:
        try:
            probes = [
                ProbeResponse(
                    id=probe.id, x=probe.x, y=probe.y, direction=probe.direction
                )
                for probe in await self.repository.find_all()
            ]
            return CheckResponse(probes=list(probes))
        except Exception:
            raise HTTPException(
                status_code=500,
                detail={
                    "code": "CHECK_UNEXPECTED_ERROR",
                    "message": "Unexpected error. Try again in a few seconds.",
                },
            )
