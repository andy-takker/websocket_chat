from websocket_chat.application.errors import (
    IncorrectCredentialsException,
    ObjectNotFoundException,
)
from websocket_chat.application.use_case import IUseCase
from websocket_chat.domain.entities.token import TokenPair, TokenPayload
from websocket_chat.domain.entities.user import LoginUser
from websocket_chat.domain.interfaces.device_repository import IDeviceRepository
from websocket_chat.domain.interfaces.password_manager import IPasswordManager
from websocket_chat.domain.interfaces.refresh_token_storage import IRefreshTokenStorage
from websocket_chat.domain.interfaces.token_service import ITokenService
from websocket_chat.domain.interfaces.user_repository import IUserRepository
from websocket_chat.domain.uow import AbstractUow


class LoginUserUseCase(IUseCase[LoginUser, TokenPair]):
    def __init__(
        self,
        user_repository: IUserRepository,
        device_repository: IDeviceRepository,
        password_manager: IPasswordManager,
        token_service: ITokenService,
        refresh_token_storage: IRefreshTokenStorage,
        uow: AbstractUow,
    ) -> None:
        self._user_repository = user_repository
        self._device_repository = device_repository
        self._password_manager = password_manager
        self._token_service = token_service
        self._refresh_token_storage = refresh_token_storage
        self._uow = uow

    async def execute(self, input_dto: LoginUser) -> TokenPair:
        async with self._uow:
            user = await self._user_repository.fetch_user_by_email(
                email=input_dto.email
            )
            if user is None:
                raise ObjectNotFoundException(
                    message=f"User with email {input_dto.email} not found"
                )

            if not self._password_manager.verify_password(
                plain_password=input_dto.password, hashed_password=user.hashed_password
            ):
                raise IncorrectCredentialsException(
                    message="Incorrect email or password"
                )

            await self._device_repository.create_or_update_device(
                device_id=input_dto.device_id,
                user_id=user.id,
            )

        access_token = await self._token_service.create_access_token(
            token_payload=TokenPayload(user_id=user.id, device_id=input_dto.device_id)
        )
        refresh_token = await self._token_service.create_refresh_token(
            token_payload=TokenPayload(user_id=user.id, device_id=input_dto.device_id)
        )
        await self._refresh_token_storage.save_refresh_token(
            device_id=input_dto.device_id,
            token=refresh_token,
        )
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )
