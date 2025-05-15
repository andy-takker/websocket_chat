from collections.abc import AsyncIterator

from dishka import AnyOf, BaseScope, Component, Provider, Scope, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from websocket_chat.adapters.database.config import DatabaseConfig
from websocket_chat.adapters.database.repositories.chat import PGChatRepository
from websocket_chat.adapters.database.repositories.device import PGDeviceRepository
from websocket_chat.adapters.database.repositories.message import PGMessageRepository
from websocket_chat.adapters.database.repositories.user import (
    PGUserRepository,
)
from websocket_chat.adapters.database.uow import SqlalchemyUow
from websocket_chat.adapters.database.utils import create_engine, create_sessionmaker
from websocket_chat.adapters.jwt_token_manager import JWTConfig, JWTTokenManager
from websocket_chat.adapters.password_manager import PasswordManager
from websocket_chat.adapters.redis_refresh_token_storage import (
    RedisConfig,
    RedisRefreshTokenStorage,
)
from websocket_chat.domain.interfaces.chat_repository import IChatRepository
from websocket_chat.domain.interfaces.device_repository import IDeviceRepository
from websocket_chat.domain.interfaces.message_repository import IMessageRepository
from websocket_chat.domain.interfaces.password_manager import IPasswordManager
from websocket_chat.domain.interfaces.refresh_token_storage import IRefreshTokenStorage
from websocket_chat.domain.interfaces.token_manager import ITokenManager
from websocket_chat.domain.interfaces.user_repository import IUserRepository
from websocket_chat.domain.uow import AbstractUow


class AdaptersProvider(Provider):
    def __init__(
        self,
        database_config: DatabaseConfig,
        jwt_config: JWTConfig,
        redis_config: RedisConfig,
        debug: bool = False,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ):
        super().__init__(scope, component)
        self.__database_config = database_config
        self.__jwt_config = jwt_config
        self.__redis_config = redis_config
        self.__debug = debug

    @provide(scope=Scope.APP)
    def password_manager(self) -> IPasswordManager:
        return PasswordManager()

    @provide(scope=Scope.APP)
    def jwt_token_manager(self) -> ITokenManager:
        return JWTTokenManager(
            secret_key=self.__jwt_config.secret_key,
            algorithm=self.__jwt_config.algorithm,
            access_token_expires_seconds=self.__jwt_config.access_token_expires_seconds,
            refresh_token_expires_seconds=self.__jwt_config.refresh_token_expires_seconds,
        )

    @provide(scope=Scope.APP)
    async def redis(self) -> AsyncIterator[Redis]:
        redis = Redis.from_url(self.__redis_config.redis_dsn)
        yield redis
        await redis.aclose(close_connection_pool=True)

    @provide(scope=Scope.APP)
    def redis_refresh_token_storage(self, redis: Redis) -> IRefreshTokenStorage:
        return RedisRefreshTokenStorage(
            redis=redis,
            ttl=self.__jwt_config.refresh_token_expires_seconds,
        )

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        async with create_engine(
            dsn=self.__database_config.dsn,
            pool_size=self.__database_config.pool_size,
            pool_timeout=self.__database_config.pool_timeout,
            max_overflow=self.__database_config.max_overflow,
            debug=self.__debug,
        ) as engine:
            yield engine

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_sessionmaker(engine=engine)

    @provide(scope=Scope.REQUEST)
    def uow(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AnyOf[AbstractUow, SqlalchemyUow]:
        return SqlalchemyUow(session_factory=session_factory)

    @provide(scope=Scope.REQUEST)
    def user_repository(
        self, uow: SqlalchemyUow
    ) -> AnyOf[IUserRepository, PGUserRepository]:
        return PGUserRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    def device_repository(
        self, uow: SqlalchemyUow
    ) -> AnyOf[IDeviceRepository, PGDeviceRepository]:
        return PGDeviceRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    def chat_repository(
        self, uow: SqlalchemyUow
    ) -> AnyOf[IChatRepository, PGChatRepository]:
        return PGChatRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    def message_repository(
        self, uow: SqlalchemyUow
    ) -> AnyOf[IMessageRepository, PGMessageRepository]:
        return PGMessageRepository(uow=uow)
