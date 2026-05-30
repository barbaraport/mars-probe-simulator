from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.direction import Direction


class MoveRequest(BaseModel):
    id: UUID
    command: str = Field(...)


class MoveResponse(BaseModel):
    id: UUID
    x: int
    y: int
    direction: Direction
