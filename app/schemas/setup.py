from pydantic import BaseModel, Field

from app.schemas.direction import Direction
from app.schemas.probe import ProbeResponse


class SetupRequest(BaseModel):
    x: int = Field(..., gt=0)
    y: int = Field(..., gt=0)
    direction: Direction


class SetupResponse(ProbeResponse):
    pass
