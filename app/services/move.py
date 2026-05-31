from app.domain.probe.entities.probe import Probe as DomainProbe
from app.domain.probe.entities.grid import Grid
from app.domain.probe.exceptions import InvalidCommandError, InvalidMovementError
from app.domain.services.CommandRunner import CommandRunner
from app.models.Probe import Probe as ModelProbe
from app.repositories.probe import ProbeRepository
from app.schemas.move import MoveResponse, MoveRequest
from fastapi import HTTPException


class MoveService:
    def __init__(
        self,
        repository: ProbeRepository,
    ) -> None:
        self.repository = repository

    async def process(
        self,
        move: MoveRequest,
    ) -> MoveResponse:
        probe = await self.repository.find_by_id(move.id)

        if probe is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "PROBE_NOT_FOUND",
                    "message": f"Probe {move.id} not found.",
                },
            )

        grid = probe.grid

        command_runner = CommandRunner(grid=Grid(x_size=grid.x, y_size=grid.y))

        try:
            new_probe = command_runner.run(
                probe=DomainProbe(x=probe.x, y=probe.y, direction=probe.direction),
                commands=move.command,
            )

            persisted_probe = await self.repository.save(
                probe=ModelProbe(
                    id=probe.id,
                    x=new_probe.x,
                    y=new_probe.y,
                    direction=new_probe.direction,
                )
            )

            return MoveResponse(
                id=persisted_probe.id,
                x=persisted_probe.x,
                y=persisted_probe.y,
                direction=persisted_probe.direction,
            )
        except InvalidCommandError as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_COMMAND_ERROR",
                    "message": f"{e} For security, no commands were delivered to the probe.",
                },
            )
        except InvalidMovementError as e:
            raise HTTPException(
                status_code=422,
                detail={
                    "code": "INVALID_MOVEMENT_ERROR",
                    "message": f"{e} For security, no commands were delivered to the probe.",
                },
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail={
                    "code": "UNEXPECTED_ERROR",
                    "message": "Unexpected error. Try again. For security, no commands were delivered to the probe.",
                },
            )
