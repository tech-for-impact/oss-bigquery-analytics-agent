
from fastapi import APIRouter

router = APIRouter()
router = APIRouter(
    prefix="/health-check",
    tags=["health-check"],
    responses={404: {"description": "Not found"}},
)

@router.get("")
async def health_check():
    return {"status": "ok"}