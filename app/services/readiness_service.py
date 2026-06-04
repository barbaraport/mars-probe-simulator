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
        try:
            is_ready = await self.repository.is_ready()

            if is_ready:
                return ReadinessResponse(api="ok", database="ok")
            else:
                return ReadinessResponse(api="ok", database="not ready")
        except Exception:
            raise HTTPException(
                status_code=500,
                detail={
                    "code": "READINESS_UNEXPECTED_ERROR",
                    "message": "Unexpected error. Try again in a few seconds.",
                },
            )
