from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.direction import Direction


class MoveRequest(BaseModel):
    id: UUID = Field(..., description="Saved probe UUID")
    command: str = Field(
        ...,
        description="Commands to run on the probe. Available commands: M (move forward, according to current probe's cardinal orientation), L (turn left), R (turn right). Note: in case of invalid commands or commands with invalid outcomes, no changes will be applied on the probe state.",
        min_length=1,
    )

    model_config = ConfigDict(str_strip_whitespace=True)


class MoveResponse(BaseModel):
    id: UUID = Field(..., description="Saved probe UUID")
    x: int = Field(
        ..., ge=0, description="Probe `x` position, greater than or equal to zero."
    )
    y: int = Field(
        ..., ge=0, description="Probe `y` position, greater than or equal to zero."
    )
    direction: Direction = Field(..., description="Probe cardinal orientation.")
