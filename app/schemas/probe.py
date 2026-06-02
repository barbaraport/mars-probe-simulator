from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.direction import Direction


class ProbeResponse(BaseModel):
    id: UUID = Field(..., description="Saved probe UUID")
    x: int = Field(
        ..., ge=0, description="Probe `x` position, greater than or equal to zero."
    )
    y: int = Field(
        ..., ge=0, description="Probe `y` position, greater than or equal to zero."
    )
    direction: Direction = Field(..., description="Probe cardinal orientation.")
