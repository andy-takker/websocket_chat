import pytest

from websocket_chat.adapters.jwt_token_service import JWTConfig, JWTTokenService


@pytest.fixture
def jwt_config() -> JWTConfig:
    return JWTConfig()


@pytest.fixture
def jwt_token_service(jwt_config: JWTConfig) -> JWTTokenService:
    return JWTTokenService(
        secret_key=jwt_config.secret_key,
        algorithm=jwt_config.algorithm,
        access_token_expires_seconds=jwt_config.access_token_expires_seconds,
        refresh_token_expires_seconds=jwt_config.refresh_token_expires_seconds,
    )
