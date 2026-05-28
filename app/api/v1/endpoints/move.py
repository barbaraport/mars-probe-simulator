from fastapi import APIRouter

move_router = APIRouter()


@move_router.post("")
async def move_probe():
    return
