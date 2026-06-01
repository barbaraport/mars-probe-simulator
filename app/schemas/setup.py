from pydantic import BaseModel, Field, model_validator

from app.schemas.direction import Direction
from app.schemas.probe import ProbeResponse


class SetupRequest(BaseModel):
    x: int = Field(..., ge=0, description="Grid `x` size, greater than or equal zero.")
    y: int = Field(..., ge=0, description="Grid `y` size, greater than or equal zero.")
    direction: Direction = Field(..., description="Initial probe cardinal orientation.")

    @model_validator(mode="after")
    def validate_grid_size(self):
        if self.x == 0 and self.y == 0:
            raise ValueError("X and Y cannot both be zero")
        return self


class SetupResponse(ProbeResponse):
    pass
