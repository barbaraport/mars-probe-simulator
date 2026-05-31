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
        "Create a new Mars probe on the grid using the SetupService. "
        "The request body must include `x`, `y`, and `direction`. "
        "The `x` and `y` values specify the size of the grid, while `direction` sets the probe's initial cardinal orientation. "
        "The probe is placed at the origin coordinate `(0, 0)` within that grid. "
        "This endpoint delegates creation to the service layer and returns the created probe state as a SetupResponse. "
        "Under the hood, the SetupService uses ProbeRepository to persist the probe and its grid position."
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
    return await service.setup(setup)
