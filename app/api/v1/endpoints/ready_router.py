from fastapi import APIRouter
from app.api.v1.dependencies import ReadyServiceDependency
from app.schemas.ready import ReadyResponse

ready_router = APIRouter()


@ready_router.get(
    "",
    response_model=ReadyResponse,
    summary="Check application readiness",
    response_description="Indicates whether the application is ready to serve requests.",
    description=(
        "Perform a readiness check to verify that the application is fully initialized and can handle requests. "
        "This endpoint can be used for monitoring and alerting purposes to ensure the service is operational."
    ),
    responses={
        200: {
            "description": "Readiness check successful",
            "model": ReadyResponse,
        },
    },
)
async def ready_check(service: ReadyServiceDependency):
    """
    Check the readiness of the application.
    """
    return await service.readiness_check()
