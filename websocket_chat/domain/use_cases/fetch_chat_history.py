from websocket_chat.application.errors import ObjectNotFoundException
from websocket_chat.application.use_case import IUseCase
from websocket_chat.domain.entities.chat import ChatHistory, FetchChatHistory
from websocket_chat.domain.interfaces.chat_repository import IChatRepository
from websocket_chat.domain.interfaces.message_repository import IMessageRepository
from websocket_chat.domain.uow import AbstractUow


class FetchChatHistoryUseCase(IUseCase[FetchChatHistory, ChatHistory]):
    def __init__(
        self,
        uow: AbstractUow,
        chat_repository: IChatRepository,
        message_repository: IMessageRepository,
    ):
        self.__uow = uow
        self.__chat_repository = chat_repository
        self.__message_repository = message_repository

    async def execute(self, input_dto: FetchChatHistory) -> ChatHistory:
        async with self.__uow:
            is_exists = await self.__chat_repository.exists_by_id(
                chat_id=input_dto.chat_id
            )
            if not is_exists:
                raise ObjectNotFoundException(
                    message=f"Chat {input_dto.chat_id} not found"
                )
            total = await self.__message_repository.count_chat_messages(
                chat_id=input_dto.chat_id
            )
            messages = await self.__message_repository.fetch_chat_messages(
                chat_id=input_dto.chat_id,
                limit=input_dto.limit,
                offset=input_dto.offset,
            )
            return ChatHistory(
                chat_id=input_dto.chat_id,
                total=total,
                messages=messages,
            )
