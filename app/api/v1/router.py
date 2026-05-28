from fastapi import APIRouter
from .endpoints.setup import setup_router
from .endpoints.move import move_router
from .endpoints.check import check_router


api_router = APIRouter()
api_router.include_router(setup_router, prefix="/setup", tags=["setup"])
api_router.include_router(move_router, prefix="/move", tags=["move"])
api_router.include_router(check_router, prefix="/check", tags=["check"])
