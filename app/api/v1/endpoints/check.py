from fastapi import APIRouter

check_router = APIRouter()


@check_router.post("")
async def check_probes():
    return
