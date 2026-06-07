from app.core.events import ProbeEvents
from app.core.logging import Logger
from app.core.observability import Observability
from app.domain.probe.entities.probe import Probe as DomainProbe
from app.domain.probe.entities.grid import Grid
from app.domain.probe.exceptions import InvalidCommandError, InvalidMovementError
from app.domain.services.CommandRunner import CommandRunner
from app.models.Probe import Probe as ModelProbe
from app.repositories.probe_repository import ProbeRepository
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

        try:
            command_runner = CommandRunner(grid=Grid(x_size=grid.x, y_size=grid.y))
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

            Observability.emit(
                ProbeEvents.PROBE_COMMAND_SENT,
                probe_id=probe.id,
                command=move.command,
                from_x=probe.x,
                from_y=probe.y,
                from_direction=probe.direction,
                to_x=persisted_probe.x,
                to_y=persisted_probe.y,
                to_direction=persisted_probe.direction,
            )

            return MoveResponse(
                id=persisted_probe.id,
                x=persisted_probe.x,
                y=persisted_probe.y,
                direction=persisted_probe.direction,
            )
        except InvalidCommandError as e:
            Observability.emit(
                ProbeEvents.PROBE_INVALID_COMMAND,
                probe_id=probe.id,
                command=move.command,
            )
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_COMMAND_ERROR",
                    "message": f"{e} For security, no commands were delivered to the probe.",
                },
            )
        except InvalidMovementError as e:
            Observability.emit(
                ProbeEvents.PROBE_INVALID_COMMAND,
                probe_id=probe.id,
                command=move.command,
                from_x=probe.x,
                from_y=probe.y,
                from_direction=probe.direction,
                grid_x=grid.x,
                grid_y=grid.y,
            )

            raise HTTPException(
                status_code=422,
                detail={
                    "code": "INVALID_MOVEMENT_ERROR",
                    "message": f"{e} For security, no commands were delivered to the probe.",
                },
            )
        except Exception:
            Logger.log(
                "move_unexpected_error",
                probe_id=probe.id,
                command=move.command,
            )
            raise HTTPException(
                status_code=500,
                detail={
                    "code": "MOVE_UNEXPECTED_ERROR",
                    "message": "Unexpected error. Try again. For security, no commands were delivered to the probe.",
                },
            )
