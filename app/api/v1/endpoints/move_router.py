from fastapi import APIRouter

from app.api.v1.dependencies import MoveServiceDependency
from app.schemas.move import MoveRequest, MoveResponse

move_router = APIRouter()


@move_router.patch(
    "",
    response_model=MoveResponse,
    summary="Move probe on the grid",
    description="Move a probe on the Martian grid based on a command string.\n\n"
    "## Validations\n\n"
    "The endpoint performs comprehensive validation of the move command before applying any changes to the probe state:\n\n"
    "- **Command Validation**: Ensures the command string contains only valid commands (L, R, M).\n"
    "- **Movement Validation**: Verifies that the probe stays within grid boundaries and doesn't attempt invalid movements.\n\n"
    "## Error Handling\n\n"
    "In case of validation errors, **no commands are applied to the probe state**, ensuring data integrity and security.\n\n"
    "This is guaranteed for all error scenarios:\n"
    "- Invalid command format or unsupported commands\n"
    "- Movement that would take the probe outside the grid boundaries\n"
    "- Any unexpected errors\n\n"
    "The probe state remains unchanged if any error occurs during command execution.",
    status_code=200,
    responses={
        200: {
            "description": "Probe moved successfully",
            "model": MoveResponse,
        },
        400: {
            "description": "Invalid command error - unsupported or malformed command string. Probe state unchanged.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "INVALID_COMMAND_ERROR",
                            "message": "Invalid command: X. For security, no commands were delivered to the probe.",
                        }
                    }
                }
            },
        },
        404: {
            "description": "Probe not found with the given ID.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "PROBE_NOT_FOUND",
                            "message": "Probe {id} not found.",
                        }
                    }
                }
            },
        },
        422: {
            "description": "Invalid movement error - probe would move outside grid boundaries. Probe state unchanged.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "INVALID_MOVEMENT_ERROR",
                            "message": "Movement would place probe outside grid. For security, no commands were delivered to the probe.",
                        }
                    }
                }
            },
        },
        500: {
            "description": "Unexpected server error. Probe state unchanged.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "UNEXPECTED_ERROR",
                            "message": "Unexpected error. Try again. For security, no commands were delivered to the probe.",
                        }
                    }
                }
            },
        },
    },
)
async def move_probe(move: MoveRequest, service: MoveServiceDependency):
    """
    Execute a move command on a probe.
    """
    return await service.move(move)
