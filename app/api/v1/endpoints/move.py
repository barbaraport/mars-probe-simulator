from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.database import get_session
from app.repositories.probe import ProbeRepository
from app.schemas.move import MoveRequest, MoveResponse
from app.services.move import MoveService
from sqlalchemy.ext.asyncio import AsyncSession

move_router = APIRouter()


AsyncSessionDependency = Annotated[AsyncSession, Depends(get_session)]


def get_probe_repository(session: AsyncSessionDependency) -> ProbeRepository:
    return ProbeRepository(session=session)


ProbeRepositoryDependency = Annotated[ProbeRepository, Depends(get_probe_repository)]


def get_move_service(repository: ProbeRepositoryDependency) -> MoveService:
    return MoveService(repository)


MoveServiceDependency = Annotated[
    MoveService,
    Depends(get_move_service),
]


@move_router.post("", response_model=MoveResponse)
async def move_probe(move: MoveRequest, service: MoveServiceDependency):
    return await service.process(move)
