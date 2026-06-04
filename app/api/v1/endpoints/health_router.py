from fastapi import APIRouter
from app.schemas.health import HealthResponse

health_router = APIRouter()


@health_router.get(
    "",
    response_model=HealthResponse,
    summary="Check application health",
    response_description="Indicates whether the application is functioning correctly.",
    description=(
        "Perform a health check to verify that the application is running and responsive. "
        "This endpoint can be used for monitoring and alerting purposes to ensure the service is operational."
    ),
    responses={
        200: {
            "description": "Health check successful",
            "model": HealthResponse,
        },
    },
)
async def health_check():
    """
    Check the health of the application.
    """
    return HealthResponse(status="ok")
