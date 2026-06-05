from app.schemas.readiness import ReadinessResponse
from app.repositories.probe_repository import ProbeRepository
from fastapi import HTTPException


class ReadinessService:
    def __init__(
        self,
        repository: ProbeRepository,
    ) -> None:
        self.repository = repository

    async def readiness_check(self) -> ReadinessResponse:
        is_ready = await self.repository.is_ready()

        if is_ready:
            return ReadinessResponse(api="ok", database="ok")
        else:
            raise HTTPException(
                status_code=503,
                detail={
                    "code": "SERVICE_NOT_READY",
                    "message": "Service is not ready. Database connection unavailable.",
                },
            )
