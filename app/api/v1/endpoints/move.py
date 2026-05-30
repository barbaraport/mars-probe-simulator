from fastapi import APIRouter

from app.api.v1.dependencies import MoveServiceDependency
from app.schemas.move import MoveRequest, MoveResponse

move_router = APIRouter()


@move_router.post("", response_model=MoveResponse)
async def move_probe(move: MoveRequest, service: MoveServiceDependency):
    return await service.process(move)
