from app.schemas.ready import ReadyResponse
from app.repositories.probe_repository import ProbeRepository
from fastapi import HTTPException


class ReadyService:
    def __init__(
        self,
        repository: ProbeRepository,
    ) -> None:
        self.repository = repository

    async def process(self) -> ReadyResponse:
        is_ready = await self.repository.is_ready()

        if is_ready:
            return ReadyResponse(api=True, database=True)
        else:
            raise HTTPException(
                status_code=503,
                detail={
                    "code": "SERVICE_NOT_READY",
                    "message": "Service is not ready. Database connection unavailable.",
                },
            )
