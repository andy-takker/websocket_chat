from uuid import UUID

import pytest
from dirty_equals import IsPartialDict
from jose import JWTError, jwt

from websocket_chat.adapters.jwt_token_service import JWTConfig, JWTTokenService, Scopes
from websocket_chat.domain.entities.token import TokenPayload


async def test_create_access_token(
    jwt_token_service: JWTTokenService,
    jwt_config: JWTConfig,
):
    user_id = UUID(int=1)
    device_id = UUID(int=1)

    token_payload = TokenPayload(
        user_id=user_id,
        device_id=device_id,
    )

    access_token = await jwt_token_service.create_access_token(
        token_payload=token_payload
    )

    assert jwt.decode(
        access_token,
        jwt_config.secret_key,
    ) == IsPartialDict(
        {
            "sub": str(user_id),
            "did": str(device_id),
            "scope": Scopes.ACCESS,
        }
    )


async def test_create_refresh_token(
    jwt_token_service: JWTTokenService,
    jwt_config: JWTConfig,
):
    user_id = UUID(int=1)
    device_id = UUID(int=1)

    token_payload = TokenPayload(
        user_id=user_id,
        device_id=device_id,
    )

    refresh_token = await jwt_token_service.create_refresh_token(
        token_payload=token_payload
    )

    assert jwt.decode(
        refresh_token,
        jwt_config.secret_key,
    ) == IsPartialDict(
        {
            "sub": str(user_id),
            "did": str(device_id),
            "scope": Scopes.REFRESH,
        }
    )


async def test_verify_access_token__success(
    jwt_token_service: JWTTokenService,
):
    user_id = UUID(int=1)
    device_id = UUID(int=1)
    token_payload = TokenPayload(
        user_id=user_id,
        device_id=device_id,
    )
    access_token = await jwt_token_service.create_access_token(
        token_payload=token_payload
    )

    assert (
        await jwt_token_service.verify_access_token(token=access_token) == token_payload
    )


async def test_verify_access_token__error(
    jwt_token_service: JWTTokenService,
):
    access_token = "token"

    with pytest.raises(JWTError):
        await jwt_token_service.verify_access_token(token=access_token)


async def test_verify_refresh_token__success(
    jwt_token_service: JWTTokenService,
):
    user_id = UUID(int=1)
    device_id = UUID(int=1)
    token_payload = TokenPayload(
        user_id=user_id,
        device_id=device_id,
    )
    refresh_token = await jwt_token_service.create_refresh_token(
        token_payload=token_payload
    )

    assert (
        await jwt_token_service.verify_refresh_token(token=refresh_token)
        == token_payload
    )


async def test_verify_refresh_token__error(
    jwt_token_service: JWTTokenService,
):
    refresh_token = "token"

    with pytest.raises(JWTError):
        await jwt_token_service.verify_refresh_token(token=refresh_token)
