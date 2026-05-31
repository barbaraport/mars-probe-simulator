from typing import Annotated

from fastapi import Depends

from app.core.database import get_session
from app.repositories.probe_repository import ProbeRepository
from app.services.check_service import CheckService
from app.services.move_service import MoveService
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.setup_service import SetupService


AsyncSessionDependency = Annotated[AsyncSession, Depends(get_session)]


def get_probe_repository(session: AsyncSessionDependency) -> ProbeRepository:
    return ProbeRepository(session=session)


ProbeRepositoryDependency = Annotated[ProbeRepository, Depends(get_probe_repository)]


def get_setup_service(repository: ProbeRepositoryDependency) -> SetupService:
    return SetupService(repository)


def get_move_service(repository: ProbeRepositoryDependency) -> MoveService:
    return MoveService(repository)


def get_check_service(repository: ProbeRepositoryDependency) -> CheckService:
    return CheckService(repository)


MoveServiceDependency = Annotated[
    MoveService,
    Depends(get_move_service),
]

CheckServiceDependency = Annotated[
    CheckService,
    Depends(get_check_service),
]

SetupServiceDependency = Annotated[
    SetupService,
    Depends(get_setup_service),
]
