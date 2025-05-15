from fastapi import APIRouter

from websocket_chat.presentors.web.routers.api.v1.auth import (
    router as auth_router,
)
from websocket_chat.presentors.web.routers.api.v1.chat import (
    router as chat_router,
)
from websocket_chat.presentors.web.routers.api.v1.monitoring import (
    router as monitoring_router,
)

router = APIRouter(prefix="/v1")
router.include_router(auth_router.router)
router.include_router(chat_router.router)
router.include_router(monitoring_router.router)
