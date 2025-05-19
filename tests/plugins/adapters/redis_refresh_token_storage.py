import pytest
from redis.asyncio import Redis

from websocket_chat.adapters.jwt_token_manager import JWTConfig
from websocket_chat.adapters.redis_refresh_token_storage import (
    RedisRefreshTokenStorage,
)
from websocket_chat.domain.interfaces.token_service import ITokenService


@pytest.fixture
def redis_refresh_token_prefix() -> str:
    return "refresh:"


@pytest.fixture
def redis_refresh_token_storage(
    redis: Redis,
    jwt_config: JWTConfig,
    redis_refresh_token_prefix: str,
    jwt_token_service: ITokenService,
) -> RedisRefreshTokenStorage:
    return RedisRefreshTokenStorage(
        redis=redis,
        ttl=jwt_config.refresh_token_expires_seconds,
        prefix=redis_refresh_token_prefix,
        token_service=jwt_token_service,
    )
