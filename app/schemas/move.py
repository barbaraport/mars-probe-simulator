from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.direction import Direction


class MoveRequest(BaseModel):
    id: UUID = Field(..., description="Saved probe UUID")
    command: str = Field(
        ...,
        description="Commands to run on the probe. Available commands: M (move forward, according to current probe's cardinal orientation), L (turn left), R (turn right). Note: in case of invalid commands or commands with invalid outcomes, no changes will be applied on the probe state.",
    )


class MoveResponse(BaseModel):
    id: UUID = Field(..., description="Saved probe UUID")
    x: int = Field(..., ge=0, description="Grid `x` size, greater than or equal zero.")
    y: int = Field(..., ge=0, description="Grid `y` size, greater than or equal zero.")
    direction: Direction = Field(..., description="Initial probe cardinal orientation.")
