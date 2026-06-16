from fastapi import APIRouter
from app.api.v1.dependencies import CheckServiceDependency
from app.schemas.check import CheckResponse

check_router = APIRouter()


@check_router.get(
    "",
    response_model=CheckResponse,
    summary="Retrieve current Mars probe positions",
    response_description="A list of all stored probes with their current coordinates and direction.",
    description=(
        "Fetch the current state of every probe from the repository via the CheckService. "
        "This endpoint uses the service layer to load probe entities from the repository, "
        "transform them into response models, and return their current position and direction."
    ),
    responses={
        200: {
            "description": "Probes fetched successfully",
            "model": CheckResponse,
        },
        500: {
            "description": "Unexpected server error.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "CHECK_UNEXPECTED_ERROR",
                            "message": "Unexpected error. Try again in a few seconds.",
                        }
                    }
                }
            },
        },
    },
)
async def check_probes(service: CheckServiceDependency):
    """
    Get the current position and orientation of all Mars probes.
    """
    return await service.process()
