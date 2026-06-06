from fastapi import APIRouter

from app.api.v1.endpoints.ready_router import ready_router
from app.api.v1.endpoints.setup_router import setup_router
from app.api.v1.endpoints.move_router import move_router
from app.api.v1.endpoints.check_router import check_router


api_router = APIRouter()
api_router.include_router(ready_router, prefix="/readiness", tags=["Readiness check"])
api_router.include_router(
    setup_router, prefix="/setup", tags=["Setup probe and its grid"]
)
api_router.include_router(move_router, prefix="/move", tags=["Move probe"])
api_router.include_router(check_router, prefix="/check", tags=["Check all probes"])
