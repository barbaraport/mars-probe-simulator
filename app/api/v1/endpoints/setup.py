from typing import Annotated

from fastapi import APIRouter, Depends
from app.core.database import get_session
from app.repositories.probe import ProbeRepository
from app.schemas.setup import SetupRequest, SetupResponse
from app.services.setup import SetupService
from sqlalchemy.ext.asyncio import AsyncSession


setup_router = APIRouter()


AsyncSessionDependency = Annotated[AsyncSession, Depends(get_session)]


def get_probe_repository(session: AsyncSessionDependency) -> ProbeRepository:
    return ProbeRepository(session=session)


ProbeRepositoryDependency = Annotated[ProbeRepository, Depends(get_probe_repository)]


def get_setup_service(repository: ProbeRepositoryDependency) -> SetupService:
    return SetupService(repository)


SetupServiceDependency = Annotated[
    SetupService,
    Depends(get_setup_service),
]


@setup_router.post("", response_model=SetupResponse)
async def setup_probe(setup: SetupRequest, service: SetupServiceDependency):
    return await service.process(setup)
