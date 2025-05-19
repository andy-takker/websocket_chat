from dataclasses import dataclass, field
from os import environ
from typing import Final
from uuid import UUID

from redis.asyncio import Redis

from websocket_chat.domain.interfaces.refresh_token_storage import IRefreshTokenStorage
from websocket_chat.domain.interfaces.token_service import ITokenService

DEFAULT_REFRESH_PREFIX: Final[str] = "refresh:"


class RedisRefreshTokenStorage(IRefreshTokenStorage):
    def __init__(
        self,
        redis: Redis,
        ttl: int,
        token_service: ITokenService,
        prefix: str = DEFAULT_REFRESH_PREFIX,
    ) -> None:
        self._redis = redis
        self._ttl = ttl
        self._prefix = prefix
        self._token_service = token_service

    async def get_refresh_token(self, *, device_id: UUID) -> str | None:
        return await self._redis.get(f"{self._prefix}{device_id}")

    async def save_refresh_token(self, *, device_id: UUID, token: str) -> None:
        await self._redis.set(f"{self._prefix}{device_id}", token, ex=self._ttl)

    async def del_refresh_token(self, *, device_id: UUID) -> None:
        await self._redis.delete(f"{self._prefix}{device_id}")

    async def del_all_refresh_tokens(self, *, user_id: UUID) -> None:
        async for key in self._redis.scan_iter(match=f"{self._prefix}*"):
            token = await self._redis.get(key)
            if token is None:
                continue
            try:
                token_payload = await self._token_service.verify_refresh_token(
                    token=token
                )
            except Exception:  # noqa: BLE001
                continue
            if token_payload.user_id == user_id:
                await self._redis.delete(key)


@dataclass(frozen=True, kw_only=True, slots=True)
class RedisConfig:
    redis_dsn: str = field(default_factory=lambda: environ["APP_REDIS_DSN"])
