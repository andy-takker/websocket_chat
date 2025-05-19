from uuid import UUID

from redis.asyncio import Redis

from websocket_chat.adapters.redis_refresh_token_storage import RedisRefreshTokenStorage
from websocket_chat.domain.entities.token import TokenPayload
from websocket_chat.domain.interfaces.token_service import ITokenService


async def test_save_refresh_token(
    redis_refresh_token_storage: RedisRefreshTokenStorage,
    redis_refresh_token_prefix: str,
    redis: Redis,
):
    token = "token"
    device_id = UUID(int=1)

    await redis_refresh_token_storage.save_refresh_token(
        device_id=device_id,
        token=token,
    )

    assert await redis.get(f"{redis_refresh_token_prefix}{device_id}") == token.encode()


async def test_del_refresh_token(
    redis_refresh_token_storage: RedisRefreshTokenStorage,
    redis_refresh_token_prefix: str,
    redis: Redis,
):
    token = "token"
    device_id = UUID(int=1)

    await redis.set(f"{redis_refresh_token_prefix}{device_id}", token)

    await redis_refresh_token_storage.del_refresh_token(device_id=device_id)

    assert await redis.get(f"{redis_refresh_token_prefix}{device_id}") is None


async def test_get_refresh_token(
    redis_refresh_token_storage: RedisRefreshTokenStorage,
    redis_refresh_token_prefix: str,
    redis: Redis,
):
    token = "token"
    device_id = UUID(int=1)

    await redis.set(f"{redis_refresh_token_prefix}{device_id}", token)

    assert (
        await redis_refresh_token_storage.get_refresh_token(device_id=device_id)
        == token.encode()
    )


async def test_del_all_refresh_tokens__empty(
    redis_refresh_token_storage: RedisRefreshTokenStorage,
    redis: Redis,
):
    await redis_refresh_token_storage.del_all_refresh_tokens(user_id=UUID(int=1))
    assert await redis.dbsize() == 0


async def test_del_all_refresh_tokens(
    redis_refresh_token_storage: RedisRefreshTokenStorage,
    jwt_token_service: ITokenService,
    redis: Redis,
    redis_refresh_token_prefix: str,
):
    device_id = UUID(int=1)
    user_id = UUID(int=2)
    refresh_token = await jwt_token_service.create_refresh_token(
        token_payload=TokenPayload(
            user_id=user_id,
            device_id=device_id,
        )
    )
    await redis.set(f"{redis_refresh_token_prefix}{device_id}", refresh_token)

    await redis_refresh_token_storage.del_all_refresh_tokens(user_id=user_id)

    assert await redis.get(f"{redis_refresh_token_prefix}{device_id}") is None
