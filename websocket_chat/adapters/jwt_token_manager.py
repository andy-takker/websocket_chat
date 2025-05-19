import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from os import environ
from typing import Any
from uuid import UUID

from jose import JWTError, jwt

from websocket_chat.domain.entities.token import TokenPayload
from websocket_chat.domain.interfaces.token_service import ITokenService


class JWTTokenService(ITokenService):
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expires_seconds: int,
        refresh_token_expires_seconds: int,
    ):
        self.__secret_key = secret_key
        self.__algorithm = algorithm
        self.__access_token_expires_seconds = access_token_expires_seconds
        self.__refresh_token_expires_seconds = refresh_token_expires_seconds

    async def create_access_token(self, *, token_payload: TokenPayload) -> str:
        payload = {
            "sub": str(token_payload.user_id),
            "did": str(token_payload.device_id),
            "scope": "access",
        }
        return self._encode(payload, self.__access_token_expires_seconds)

    async def create_refresh_token(self, *, token_payload: TokenPayload) -> str:
        payload = {
            "sub": str(token_payload.user_id),
            "did": str(token_payload.device_id),
            "scope": "refresh",
        }
        return self._encode(payload, self.__refresh_token_expires_seconds)

    async def verify_access_token(self, *, token: str) -> TokenPayload:
        payload = self._decode(token)
        if payload.get("scope") != "access":
            raise JWTError("Expected access token")
        return TokenPayload(
            user_id=UUID(payload["sub"]),
            device_id=UUID(payload["did"]),
        )

    async def verify_refresh_token(self, *, token: str) -> TokenPayload:
        payload = self._decode(token)
        if payload.get("scope") != "refresh":
            raise JWTError("Expected refresh token")
        return TokenPayload(
            user_id=UUID(payload["sub"]),
            device_id=UUID(payload["did"]),
        )

    async def refresh_access_token(self, *, refresh_token: str) -> str:
        token_payload = await self.verify_refresh_token(token=refresh_token)
        return await self.create_access_token(token_payload=token_payload)

    def _encode(self, payload: Mapping[str, Any], exp: int) -> str:
        issued = int(time.time())
        to_encode = {**payload, "iat": issued, "exp": issued + exp}
        return jwt.encode(to_encode, self.__secret_key, algorithm=self.__algorithm)

    def _decode(self, token: str) -> Mapping[str, Any]:
        try:
            return jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
        except JWTError:
            return {}


@dataclass(frozen=True, kw_only=True, slots=True)
class JWTConfig:
    secret_key: str = field(
        default_factory=lambda: environ.get("APP_JWT_SECRET_KEY", "secret")
    )
    algorithm: str = field(
        default_factory=lambda: environ.get("APP_JWT_ALGORITHM", "HS256")
    )
    access_token_expires_seconds: int = field(
        default_factory=lambda: int(
            environ.get("APP_JWT_ACCESS_TOKEN_EXPIRES_SECONDS", 900)
        )
    )
    refresh_token_expires_seconds: int = field(
        default_factory=lambda: int(
            environ.get("APP_JWT_REFRESH_TOKEN_EXPIRES_SECONDS", 86400)
        )
    )
