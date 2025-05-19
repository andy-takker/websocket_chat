from fastapi import APIRouter

from websocket_chat.presentors.web.routers.api.v1.monitoring.models import (
    StatusModel,
    StatusType,
)

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/health")
async def health() -> StatusModel:
    return StatusModel(status=StatusType.OK)
