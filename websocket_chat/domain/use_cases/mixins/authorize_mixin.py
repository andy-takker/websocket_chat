from websocket_chat.application.errors import ObjectNotFoundException
from websocket_chat.domain.entities.user import DevicedUser
from websocket_chat.domain.interfaces.token_service import ITokenService
from websocket_chat.domain.interfaces.user_repository import IUserRepository


class AuthorizeMixin:
    _token_service: ITokenService
    _user_repository: IUserRepository

    async def _authorize(self, *, access_token: str) -> DevicedUser:
        payload = await self._token_service.verify_access_token(token=access_token)
        user = await self._user_repository.fetch_user_by_id(user_id=payload.user_id)
        if user is None:
            raise ObjectNotFoundException(message=f"User {payload.user_id} not found")
        return DevicedUser(
            id=user.id,
            name=user.name,
            email=user.email,
            device_id=payload.device_id,
            hashed_password=user.hashed_password,
        )
