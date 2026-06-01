from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.direction import Direction


class ProbeResponse(BaseModel):
    id: UUID = Field(..., description="Saved probe UUID")
    x: int = Field(..., ge=0, description="Grid `x` size, greater than or equal zero.")
    y: int = Field(..., ge=0, description="Grid `y` size, greater than or equal zero.")
    direction: Direction = Field(..., description="Initial probe cardinal orientation.")
