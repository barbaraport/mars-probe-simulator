from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.probe import ProbeRepository
from app.schemas.check import CheckResponse
from app.services.check import CheckService

check_router = APIRouter()

AsyncSessionDependency = Annotated[AsyncSession, Depends(get_session)]


def get_probe_repository(session: AsyncSessionDependency) -> ProbeRepository:
    return ProbeRepository(session=session)


ProbeRepositoryDependency = Annotated[ProbeRepository, Depends(get_probe_repository)]


def get_check_service(repository: ProbeRepositoryDependency) -> CheckService:
    return CheckService(repository)


CheckServiceDependency = Annotated[
    CheckService,
    Depends(get_check_service),
]


@check_router.post("", response_model=CheckResponse)
async def check_probes(service: CheckServiceDependency):
    return await service.check()
