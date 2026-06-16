from fastapi import APIRouter
from app.api.v1.dependencies import SetupServiceDependency
from app.schemas.setup import SetupRequest, SetupResponse


setup_router = APIRouter()


@setup_router.post(
    "",
    response_model=SetupResponse,
    status_code=200,
    summary="Initialize a Mars probe on the grid",
    response_description="Details of the newly created probe, including its generated id, coordinates, and direction.",
    description=(
        "Create a new Mars probe on the grid using the SetupService.\n\n"
        "### Request\n"
        "- `x` and `y`: grid dimensions\n"
        "- `direction`: initial cardinal orientation\n\n"
        "### Behavior\n"
        "- The probe starts at coordinate `(0, 0)` on the grid.\n"
        "- Grid dimensions must be non-negative integers, and at least one dimension must be greater than zero.\n\n"
        "### Result\n"
        "- Returns the created probe state as a `SetupResponse`.\n"
        "- The SetupService uses ProbeRepository to persist the probe and its grid position."
    ),
    responses={
        200: {
            "description": "Probe initialized successfully on valid grid",
            "model": SetupResponse,
        },
        500: {
            "description": "Unexpected server error.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "SETUP_UNEXPECTED_ERROR",
                            "message": "Unexpected error. Try again in a few seconds.",
                        }
                    }
                }
            },
        },
    },
)
async def setup_probe(setup: SetupRequest, service: SetupServiceDependency):
    """
    Initialize a Mars probe at the specified coordinates and direction.
    """
    return await service.process(setup)
