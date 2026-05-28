from typing import Annotated

from fastapi import APIRouter, Depends
from app.repositories.probe import ProbeRepository
from app.schemas.setup import SetupRequest, SetupResponse
from app.services.setup import SetupService

setup_router = APIRouter()


def get_probe_repository() -> ProbeRepository:
    return ProbeRepository()


ProbeRepositoryDependency = Annotated[ProbeRepository, Depends(get_probe_repository)]


def get_setup_service(repository: ProbeRepositoryDependency) -> SetupService:
    return SetupService(repository)


SetupServiceDependency = Annotated[
    SetupService,
    Depends(get_setup_service),
]


@setup_router.post("", response_model=SetupResponse)
async def setup_probe(setup: SetupRequest, service: SetupServiceDependency):
    return service.process(setup)
