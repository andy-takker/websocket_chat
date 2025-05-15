from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

from websocket_chat.domain.entities.chat import FetchChatHistory
from websocket_chat.domain.use_cases.fetch_chat_history import FetchChatHistoryUseCase
from websocket_chat.presentors.web.routers.api.v1.chat.models import (
    ChatHistoryResponseModel,
)

router = APIRouter(prefix="/chat", tags=["chat"], route_class=DishkaRoute)


@router.get("/history/{chat_id}")
async def fetch_chat_history_by_id(
    chat_id: UUID,
    fetch_chat_history: FromDishka[FetchChatHistoryUseCase],
    limit: int = Query(gt=0, le=100, default=100),
    offset: int = Query(ge=0, default=0),
) -> ChatHistoryResponseModel:
    chat_history = await fetch_chat_history.execute(
        input_dto=FetchChatHistory(
            chat_id=chat_id,
            limit=limit,
            offset=offset,
        ),
    )
    return ChatHistoryResponseModel.model_validate(chat_history)
