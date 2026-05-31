from app.domain.probe.entities.probe import Probe as DomainProbe
from app.domain.probe.entities.grid import Grid
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
        new_probe = command_runner.run(
            probe=DomainProbe(x=probe.x, y=probe.y, direction=probe.direction),
            commands=move.command,
        )

        persisted_probe = await self.repository.save(
            probe=ModelProbe(
                id=probe.id, x=new_probe.x, y=new_probe.y, direction=new_probe.direction
            )
        )

        return MoveResponse(
            id=persisted_probe.id,
            x=persisted_probe.x,
            y=persisted_probe.y,
            direction=persisted_probe.direction,
        )
