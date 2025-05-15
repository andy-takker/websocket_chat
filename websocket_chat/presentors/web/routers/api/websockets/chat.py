import logging
from uuid import UUID

from dishka import AsyncContainer, FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from websocket_chat.domain.entities.chat import ReadMessageDTO, SaveMessageDTO
from websocket_chat.domain.use_cases.chat_authorize import ChatAuthorizeUseCase
from websocket_chat.domain.use_cases.read_message import ReadMessageUseCase
from websocket_chat.domain.use_cases.save_message import SaveMessageUseCase
from websocket_chat.presentors.web.websocket_manager import WebsocketManager

log = logging.getLogger(__name__)

router = APIRouter(prefix="/chat/", route_class=DishkaRoute)


@router.websocket("/{chat_id}")
async def chat_ws(
    chat_id: UUID,
    ws: WebSocket,
    container: FromDishka[AsyncContainer],
    websocket_manager: FromDishka[WebsocketManager],
    token: str = Query(),
) -> None:
    async with container() as container:
        chat_auth = await container.get(ChatAuthorizeUseCase)
        user = await chat_auth.execute(input_dto=token)

    await websocket_manager.connect(
        chat_id=chat_id,
        user_id=user.id,
        device_id=user.device_id,
        ws=ws,
    )

    try:
        while True:
            data = await ws.receive_json()
            match data.get("type"):
                case "message":
                    client_id = UUID(data["client_id"])
                    text = data["text"]
                    async with container() as container:
                        save_message = await container.get(SaveMessageUseCase)
                        message = await save_message.execute(
                            input_dto=SaveMessageDTO(
                                chat_id=chat_id,
                                sender_id=client_id,
                                text=text,
                            ),
                        )
                    await websocket_manager.broadcast_chat(
                        chat_id=chat_id,
                        data={
                            "type": "message",
                            "id": message.id,
                            "chat_id": message.chat_id,
                            "sender_id": user.id,
                            "client_id": str(client_id),
                            "text": text,
                            "created_at": message.created_at.isoformat(),
                        },
                    )
                case "read":
                    message_id = UUID(data["id"])
                    async with container() as container:
                        read_message = await container.get(ReadMessageUseCase)
                        result = await read_message.execute(
                            input_dto=ReadMessageDTO(
                                chat_id=chat_id, message_id=message_id, user_id=user.id
                            ),
                        )
                        if result.ok:
                            await websocket_manager.broadcast_user(
                                chat_id=chat_id,
                                user_id=result.author_id,
                                data={
                                    "type": "read",
                                    "id": message_id,
                                    "chat_id": chat_id,
                                },
                            )
                case _:
                    await ws.send_json(
                        {
                            "type": "error",
                            "message": "Invalid message type",
                        }
                    )

    except WebSocketDisconnect:
        log.info("WebSocket disconnected")
    finally:
        websocket_manager.disconnect(
            chat_id=chat_id,
            user_id=user.id,
            device_id=user.device_id,
            ws=ws,
        )
