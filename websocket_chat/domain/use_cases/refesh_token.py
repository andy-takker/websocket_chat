from websocket_chat.application.errors import RefreshTokenNotFoundException
from websocket_chat.application.use_case import IUseCase
from websocket_chat.domain.entities.token import RefreshIn, TokenPair, TokenPayload
from websocket_chat.domain.interfaces.refresh_token_storage import IRefreshTokenStorage
from websocket_chat.domain.interfaces.token_manager import ITokenManager


class RefreshTokenUseCase(IUseCase[RefreshIn, TokenPair]):
    def __init__(
        self,
        token_manager: ITokenManager,
        refresh_token_storage: IRefreshTokenStorage,
    ) -> None:
        self.__token_manager = token_manager
        self.__refresh_token_storage = refresh_token_storage

    async def execute(self, input_dto: RefreshIn) -> TokenPair:
        payload = await self.__token_manager.verify_refresh_token(
            token=input_dto.refresh_token
        )
        stored_refresh_token = await self.__refresh_token_storage.get_refresh_token(
            device_id=payload.device_id
        )
        if stored_refresh_token != input_dto.refresh_token:
            raise RefreshTokenNotFoundException(message="Refresh token not found")
        access_token = await self.__token_manager.create_access_token(
            token_payload=TokenPayload(
                user_id=payload.user_id, device_id=payload.device_id
            )
        )
        refresh_token = await self.__token_manager.create_refresh_token(
            token_payload=TokenPayload(
                user_id=payload.user_id, device_id=payload.device_id
            )
        )
        await self.__refresh_token_storage.save_refresh_token(
            device_id=payload.device_id,
            token=refresh_token,
        )
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
