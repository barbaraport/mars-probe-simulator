from uuid import UUID
from pydantic import BaseModel

from app.schemas.direction import Direction


class ProbeResponse(BaseModel):
    id: UUID
    x: int
    y: int
    direction: Direction
