from websocket_chat.application.errors import UserAlreadyExistsException
from websocket_chat.application.use_case import IUseCase
from websocket_chat.domain.entities.token import TokenPair, TokenPayload
from websocket_chat.domain.entities.user import UserRegister
from websocket_chat.domain.interfaces.password_manager import IPasswordManager
from websocket_chat.domain.interfaces.token_manager import ITokenManager
from websocket_chat.domain.interfaces.user_repository import IUserRepository
from websocket_chat.domain.uow import AbstractUow


class RegisterUserUseCase(IUseCase[UserRegister, TokenPair]):
    __user_repository: IUserRepository

    def __init__(
        self,
        user_repository: IUserRepository,
        password_manager: IPasswordManager,
        token_manager: ITokenManager,
        uow: AbstractUow,
    ) -> None:
        self.__user_repository = user_repository
        self.__password_manager = password_manager
        self.__token_manager = token_manager
        self.__uow = uow

    async def execute(self, input_dto: UserRegister) -> TokenPair:
        async with self.__uow:
            user = await self.__user_repository.fetch_user_by_email(
                email=input_dto.email
            )
            if user is not None:
                raise UserAlreadyExistsException(
                    message=f"User with email {input_dto.email} already exists"
                )

            user = await self.__user_repository.create_user(
                name=input_dto.name,
                email=input_dto.email,
                hashed_password=self.__password_manager.hash_password(
                    password=input_dto.password
                ),
            )

        access_token = await self.__token_manager.create_access_token(
            token_payload=TokenPayload(user_id=user.id, device_id=input_dto.device_id)
        )
        refresh_token = await self.__token_manager.create_refresh_token(
            token_payload=TokenPayload(user_id=user.id, device_id=input_dto.device_id)
        )

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )
