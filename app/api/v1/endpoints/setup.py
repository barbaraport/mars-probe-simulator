from fastapi import APIRouter

setup_router = APIRouter()


@setup_router.post("")
async def setup_probe():
    return
