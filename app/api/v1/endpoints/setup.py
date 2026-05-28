from typing import Annotated

from fastapi import APIRouter, Depends
from app.schemas.setup import SetupRequest, SetupResponse
from app.services.setup import SetupService

setup_router = APIRouter()


def get_setup_service() -> SetupService:
    return SetupService()


SetupServiceDependency = Annotated[
    SetupService,
    Depends(get_setup_service),
]


@setup_router.post("", response_model=SetupResponse)
async def setup_probe(setup: SetupRequest, service: SetupServiceDependency):
    return service.process(setup)
