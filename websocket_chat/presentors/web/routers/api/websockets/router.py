from fastapi import APIRouter

from websocket_chat.presentors.web.routers.api.websockets.chat import (
    router as chat_router,
)

router = APIRouter(prefix="/ws")
router.include_router(chat_router)
