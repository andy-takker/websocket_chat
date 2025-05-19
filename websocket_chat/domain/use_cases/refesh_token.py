from websocket_chat.application.errors import RefreshTokenNotFoundException
from websocket_chat.application.use_case import IUseCase
from websocket_chat.domain.entities.token import RefreshIn, TokenPair, TokenPayload
from websocket_chat.domain.interfaces.refresh_token_storage import IRefreshTokenStorage
from websocket_chat.domain.interfaces.token_service import ITokenService


class RefreshTokenUseCase(IUseCase[RefreshIn, TokenPair]):
    def __init__(
        self,
        token_service: ITokenService,
        refresh_token_storage: IRefreshTokenStorage,
    ) -> None:
        self._token_service = token_service
        self._refresh_token_storage = refresh_token_storage

    async def execute(self, input_dto: RefreshIn) -> TokenPair:
        payload = await self._token_service.verify_refresh_token(
            token=input_dto.refresh_token
        )
        stored_refresh_token = await self._refresh_token_storage.get_refresh_token(
            device_id=payload.device_id
        )
        if stored_refresh_token != input_dto.refresh_token:
            raise RefreshTokenNotFoundException(message="Refresh token not found")
        access_token = await self._token_service.create_access_token(
            token_payload=TokenPayload(
                user_id=payload.user_id, device_id=payload.device_id
            )
        )
        refresh_token = await self._token_service.create_refresh_token(
            token_payload=TokenPayload(
                user_id=payload.user_id, device_id=payload.device_id
            )
        )
        await self._refresh_token_storage.save_refresh_token(
            device_id=payload.device_id,
            token=refresh_token,
        )
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
