from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field


class Direction(str, Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


class SetupRequest(BaseModel):
    x: int = Field(..., gt=0)
    y: int = Field(..., gt=0)
    direction: Direction


class SetupResponse(BaseModel):
    id: UUID
    x: int
    y: int
    direction: Direction
