from fastapi import APIRouter
from app.api.v1.dependencies import ReadinessServiceDependency
from app.schemas.readiness import ReadinessResponse

readiness_router = APIRouter()


@readiness_router.get(
    "",
    response_model=ReadinessResponse,
    summary="Check application readiness",
    response_description="Indicates whether the application is ready to serve requests.",
    description=(
        "Perform a readiness check to verify that the application is fully initialized and can handle requests. "
        "This endpoint can be used for monitoring and alerting purposes to ensure the service is operational."
    ),
    responses={
        200: {
            "description": "Readiness check successful",
            "model": ReadinessResponse,
        },
    },
)
async def readiness_check(service: ReadinessServiceDependency):
    """
    Check the readiness of the application.
    """
    return await service.readiness_check()
