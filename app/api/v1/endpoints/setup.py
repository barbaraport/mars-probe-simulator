from fastapi import APIRouter
from app.api.v1.dependencies import SetupServiceDependency
from app.schemas.setup import SetupRequest, SetupResponse


setup_router = APIRouter()


@setup_router.post("", response_model=SetupResponse)
async def setup_probe(setup: SetupRequest, service: SetupServiceDependency):
    return await service.process(setup)
