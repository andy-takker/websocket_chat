from dishka import Provider, Scope, provide

from websocket_chat.domain.interfaces.chat_participant_repository import (
    IChatParticipantRepository,
)
from websocket_chat.domain.interfaces.chat_repository import IChatRepository
from websocket_chat.domain.interfaces.device_repository import IDeviceRepository
from websocket_chat.domain.interfaces.message_repository import IMessageRepository
from websocket_chat.domain.interfaces.password_manager import IPasswordManager
from websocket_chat.domain.interfaces.refresh_token_storage import IRefreshTokenStorage
from websocket_chat.domain.interfaces.token_service import ITokenService
from websocket_chat.domain.interfaces.user_repository import IUserRepository
from websocket_chat.domain.uow import AbstractUow
from websocket_chat.domain.use_cases.chat_authorize import ChatAuthorizeUseCase
from websocket_chat.domain.use_cases.fetch_chat_history import FetchChatHistoryUseCase
from websocket_chat.domain.use_cases.login_user import LoginUserUseCase
from websocket_chat.domain.use_cases.refesh_token import RefreshTokenUseCase
from websocket_chat.domain.use_cases.register_user import RegisterUserUseCase


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def register_user_use_case(
        self,
        user_repository: IUserRepository,
        device_repository: IDeviceRepository,
        password_manager: IPasswordManager,
        token_service: ITokenService,
        refresh_token_storage: IRefreshTokenStorage,
        uow: AbstractUow,
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(
            user_repository=user_repository,
            device_repository=device_repository,
            password_manager=password_manager,
            token_service=token_service,
            refresh_token_storage=refresh_token_storage,
            uow=uow,
        )

    @provide(scope=Scope.REQUEST)
    def login_user_use_case(
        self,
        user_repository: IUserRepository,
        device_repository: IDeviceRepository,
        password_manager: IPasswordManager,
        token_service: ITokenService,
        refresh_token_storage: IRefreshTokenStorage,
        uow: AbstractUow,
    ) -> LoginUserUseCase:
        return LoginUserUseCase(
            user_repository=user_repository,
            device_repository=device_repository,
            password_manager=password_manager,
            token_service=token_service,
            refresh_token_storage=refresh_token_storage,
            uow=uow,
        )

    @provide(scope=Scope.REQUEST)
    def refresh_token(
        self, token_service: ITokenService, refresh_token_storage: IRefreshTokenStorage
    ) -> RefreshTokenUseCase:
        return RefreshTokenUseCase(
            token_service=token_service,
            refresh_token_storage=refresh_token_storage,
        )

    @provide(scope=Scope.REQUEST)
    def fetch_chat_history(
        self,
        uow: AbstractUow,
        chat_repository: IChatRepository,
        message_repository: IMessageRepository,
        token_service: ITokenService,
        user_repository: IUserRepository,
        chat_participant_repository: IChatParticipantRepository,
    ) -> FetchChatHistoryUseCase:
        return FetchChatHistoryUseCase(
            uow=uow,
            chat_repository=chat_repository,
            message_repository=message_repository,
            token_service=token_service,
            user_repository=user_repository,
            chat_participant_repository=chat_participant_repository,
        )

    @provide(scope=Scope.REQUEST)
    def chat_authorize(
        self,
        token_service: ITokenService,
        uow: AbstractUow,
        user_repository: IUserRepository,
    ) -> ChatAuthorizeUseCase:
        return ChatAuthorizeUseCase(
            uow=uow,
            token_service=token_service,
            user_repository=user_repository,
        )
