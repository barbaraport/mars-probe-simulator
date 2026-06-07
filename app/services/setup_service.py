from app.core.observability import Observability
from app.domain.probe.entities.grid import Grid
from app.domain.probe.exceptions import InvalidSizeError
from app.models.Probe import Probe as ModelProbe
from app.schemas.setup import SetupRequest, SetupResponse
from app.repositories.probe_repository import ProbeRepository
from fastapi import HTTPException
from app.core.events import ProbeEvents


class SetupService:
    def __init__(
        self,
        repository: ProbeRepository,
    ) -> None:
        self.repository = repository

    async def process(
        self,
        setup: SetupRequest,
    ) -> SetupResponse:
        try:
            grid = Grid(x_size=setup.x, y_size=setup.y)

            probe = await self.repository.setup(
                ModelProbe(x=grid.x_size, y=grid.y_size, direction=setup.direction)
            )

            Observability.emit(
                ProbeEvents.PROBE_CREATED,
                grid_id=str(probe.grid.id),
                grid_x=grid.x_size,
                grid_y=grid.y_size,
                probe_id=probe.id,
                probe_x=probe.x,
                probe_y=probe.y,
                probe_direction=probe.direction,
            )

            return SetupResponse(
                id=probe.id, x=probe.x, y=probe.y, direction=probe.direction
            )
        except InvalidSizeError as e:
            Observability.emit(
                ProbeEvents.PROBE_INVALID_SETUP,
                grid_x=setup.x,
                grid_y=setup.y,
                probe_direction=setup.direction,
            )
            raise HTTPException(
                status_code=422,
                detail={
                    "code": "INVALID_PROBE_SETUP",
                    "message": f"The grid size ({setup.x}, {setup.y}) is invalid. {e}",
                },
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail={
                    "code": "SETUP_UNEXPECTED_ERROR",
                    "message": "Unexpected error. Try again in a few seconds.",
                },
            )
