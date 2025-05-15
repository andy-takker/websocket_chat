from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Query

from websocket_chat.domain.entities.chat import FetchChatHistory
from websocket_chat.domain.use_cases.fetch_chat_history import FetchChatHistoryUseCase
from websocket_chat.presentors.web.routers.api.v1.chat.models import (
    ChatHistoryResponseModel,
)
from websocket_chat.presentors.web.security import OAUTH2_SCHEME

router = APIRouter(prefix="/chat", tags=["chat"], route_class=DishkaRoute)


@router.get(
    "/history/{chat_id}",
    response_model=ChatHistoryResponseModel,
    name="Fetch chat history by chat id",
    description=(
        "Fetch chat history by chat id. "
        "You need to authenticate and to be a member of the chat"
    ),
)
async def fetch_chat_history_by_id(
    chat_id: UUID,
    fetch_chat_history: FromDishka[FetchChatHistoryUseCase],
    limit: int = Query(gt=0, le=100, default=100),
    offset: int = Query(ge=0, default=0),
    access_token: str = Depends(OAUTH2_SCHEME),
) -> ChatHistoryResponseModel:
    chat_history = await fetch_chat_history.execute(
        input_dto=FetchChatHistory(
            access_token=access_token,
            chat_id=chat_id,
            limit=limit,
            offset=offset,
        ),
    )
    return ChatHistoryResponseModel.model_validate(chat_history)
