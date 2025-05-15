from websocket_chat.application.use_case import IUseCase
from websocket_chat.domain.entities.user import DevicedUser, User
from websocket_chat.domain.interfaces.token_manager import ITokenManager
from websocket_chat.domain.interfaces.user_repository import IUserRepository
from websocket_chat.domain.uow import AbstractUow
from websocket_chat.domain.use_cases.mixins import AuthorizeMixin


class ChatAuthorizeUseCase(AuthorizeMixin, IUseCase[str, User]):
    _token_manager: ITokenManager
    _user_repository: IUserRepository
    _uow: AbstractUow

    def __init__(
        self,
        uow: AbstractUow,
        token_manager: ITokenManager,
        user_repository: IUserRepository,
    ) -> None:
        self._uow = uow
        self._token_manager = token_manager
        self._user_repository = user_repository

    async def execute(self, input_dto: str) -> DevicedUser:
        async with self._uow:
            user = await self._authorize(access_token=input_dto)
        return user
