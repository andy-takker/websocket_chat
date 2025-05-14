import base64
import json
from dataclasses import dataclass, field
from os import environ
from typing import Final
from uuid import UUID

from redis.asyncio import Redis

from websocket_chat.domain.interfaces.refresh_token_storage import IRefreshTokenStorage


class RedisRefreshTokenStorage(IRefreshTokenStorage):
    REFRESH_PREFIX: Final[str] = "refresh:"

    def __init__(
        self,
        redis: Redis,
        ttl: int,
    ) -> None:
        self.__redis = redis
        self.__ttl = ttl

    async def save_refresh_token(self, *, device_id: UUID, token: str) -> None:
        await self.__redis.set(
            f"{self.REFRESH_PREFIX}{device_id}", token, ex=self.__ttl
        )

    async def del_refresh_token(self, *, device_id: UUID) -> None:
        await self.__redis.delete(f"{self.REFRESH_PREFIX}{device_id}")

    async def del_all_refresh_tokens(self, *, user_id: UUID) -> None:
        async for key in self.__redis.scan_iter(match=f"{self.REFRESH_PREFIX}*"):
            jwt = await self.__redis.get(key)
            if jwt is None:
                continue
            try:
                payload = jwt.split(".")[1] + "==="
                sub = int(json.loads(base64.urlsafe_b64decode(payload))["sub"])
            except Exception:  # noqa: BLE001
                continue
            if sub == user_id:
                await self.__redis.delete(key)

    async def get_refresh_token(self, *, device_id: UUID) -> str | None:
        return await self.__redis.get(f"{self.REFRESH_PREFIX}{device_id}")


@dataclass(frozen=True, kw_only=True, slots=True)
class RedisConfig:
    redis_dsn: str = field(default_factory=lambda: environ["APP_REDIS_DSN"])
