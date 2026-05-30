from fastapi import APIRouter
from app.api.v1.dependencies import CheckServiceDependency
from app.schemas.check import CheckResponse

check_router = APIRouter()


@check_router.post("", response_model=CheckResponse)
async def check_probes(service: CheckServiceDependency):
    return await service.check()
