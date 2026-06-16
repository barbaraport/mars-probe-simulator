from pydantic import BaseModel, Field

from app.schemas.direction import Direction
from app.schemas.probe import ProbeResponse


class SetupRequest(BaseModel):
    x: int = Field(..., ge=0, description="Grid `x` size, greater than or equal zero.")
    y: int = Field(..., ge=0, description="Grid `y` size, greater than or equal zero.")
    direction: Direction = Field(..., description="Initial probe cardinal orientation.")


class SetupResponse(ProbeResponse):
    pass
