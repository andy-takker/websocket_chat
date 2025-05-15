from websocket_chat.application.errors import (
    ForbiddenException,
    ObjectNotFoundException,
)
from websocket_chat.application.use_case import IUseCase
from websocket_chat.domain.entities.chat import ChatHistory, FetchChatHistory
from websocket_chat.domain.interfaces.chat_participant_repository import (
    IChatParticipantRepository,
)
from websocket_chat.domain.interfaces.chat_repository import IChatRepository
from websocket_chat.domain.interfaces.message_repository import IMessageRepository
from websocket_chat.domain.interfaces.token_manager import ITokenManager
from websocket_chat.domain.interfaces.user_repository import IUserRepository
from websocket_chat.domain.uow import AbstractUow
from websocket_chat.domain.use_cases.mixins import AuthorizeMixin


class FetchChatHistoryUseCase(AuthorizeMixin, IUseCase[FetchChatHistory, ChatHistory]):
    def __init__(
        self,
        uow: AbstractUow,
        chat_repository: IChatRepository,
        user_repository: IUserRepository,
        chat_participant_repository: IChatParticipantRepository,
        message_repository: IMessageRepository,
        token_manager: ITokenManager,
    ):
        self._uow = uow
        self._chat_repository = chat_repository
        self._chat_participant_repository = chat_participant_repository
        self._message_repository = message_repository
        self._token_manager = token_manager
        self._user_repository = user_repository

    async def execute(self, input_dto: FetchChatHistory) -> ChatHistory:
        async with self._uow:
            user = await self._authorize(access_token=input_dto.access_token)
            is_exists = await self._chat_repository.exists_by_id(
                chat_id=input_dto.chat_id
            )
            if not is_exists:
                raise ObjectNotFoundException(
                    message=f"Chat {input_dto.chat_id} not found"
                )
            is_chat_member = await self._chat_participant_repository.is_chat_member(
                chat_id=input_dto.chat_id, user_id=user.id
            )
            if not is_chat_member:
                raise ForbiddenException(
                    message=f"User {user.id} is not a member"
                    f" of chat {input_dto.chat_id}"
                )
            total = await self._message_repository.count_chat_messages(
                chat_id=input_dto.chat_id
            )
            messages = await self._message_repository.fetch_chat_messages(
                chat_id=input_dto.chat_id,
                limit=input_dto.limit,
                offset=input_dto.offset,
            )
            return ChatHistory(
                chat_id=input_dto.chat_id,
                total=total,
                messages=messages,
            )
