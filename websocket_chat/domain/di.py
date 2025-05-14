from dishka import Provider, Scope, provide

from websocket_chat.domain.interfaces.password_manager import IPasswordManager
from websocket_chat.domain.interfaces.token_manager import ITokenManager
from websocket_chat.domain.interfaces.user_repository import IUserRepository
from websocket_chat.domain.uow import AbstractUow
from websocket_chat.domain.use_cases.register_user import RegisterUserUseCase


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def register_user_use_case(
        self,
        user_repository: IUserRepository,
        password_manager: IPasswordManager,
        token_manager: ITokenManager,
        uow: AbstractUow,
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(
            user_repository=user_repository,
            password_manager=password_manager,
            token_manager=token_manager,
            uow=uow,
        )
