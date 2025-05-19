from collections.abc import AsyncIterator
from os import environ

import pytest
from redis.asyncio import Redis

from websocket_chat.adapters.redis_refresh_token_storage import RedisConfig


@pytest.fixture
def redis_config() -> RedisConfig:
    return RedisConfig(redis_dsn=environ.get("APP_REDIS_DSN", "redis://127.0.0.1:6379"))


@pytest.fixture
async def redis(redis_config: RedisConfig) -> AsyncIterator[Redis]:
    redis = Redis.from_url(redis_config.redis_dsn)
    await redis.flushall()
    yield redis
    await redis.aclose()
