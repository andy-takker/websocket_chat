from dataclasses import dataclass, field
from os import environ

from websocket_chat.adapters.database.config import DatabaseConfig
from websocket_chat.adapters.jwt_token_service import JWTConfig
from websocket_chat.adapters.redis_refresh_token_storage import RedisConfig
from websocket_chat.application.logging import LoggingConfig


@dataclass(frozen=True, kw_only=True, slots=True)
class AppConfig:
    title: str = field(
        default_factory=lambda: environ.get("APP_TITLE", "Websocket Chat")
    )
    description: str = field(
        default_factory=lambda: environ.get(
            "APP_DESCRIPTION", "Typical websocket chat for async messages"
        )
    )
    version: str = field(default_factory=lambda: environ.get("APP_VERSION", "1.0.0"))
    debug: bool = field(
        default_factory=lambda: environ.get("APP_DEBUG", "False").lower() == "true"
    )


@dataclass(frozen=True, kw_only=True, slots=True)
class Config:
    app: AppConfig = field(default_factory=AppConfig)
    log: LoggingConfig = field(default_factory=LoggingConfig)
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    jwt: JWTConfig = field(default_factory=JWTConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
