from fastapi import APIRouter

from websocket_chat.presentors.web.routers.api.v1.router import router as v1_router
from websocket_chat.presentors.web.routers.api.websockets.router import (
    router as ws_router,
)

router = APIRouter(prefix="/api")
router.include_router(v1_router)
router.include_router(ws_router)
