from fastapi import APIRouter

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
