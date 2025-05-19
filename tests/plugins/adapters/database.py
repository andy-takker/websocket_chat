from collections.abc import AsyncIterator
from os import environ
from types import SimpleNamespace

import pytest
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from websocket_chat.adapters.database.config import DatabaseConfig
from websocket_chat.adapters.database.tables import BaseTable
from websocket_chat.adapters.database.uow import SqlalchemyUow
from websocket_chat.adapters.database.utils import (
    create_engine,
    create_sessionmaker,
    make_alembic_config,
)


@pytest.fixture(scope="session")
def db_config() -> DatabaseConfig:
    return DatabaseConfig(
        host=environ.get("APP_DATABASE_HOST", "127.0.0.1"),
        port=int(environ.get("APP_DATABASE_PORT", 5432)),
        user=environ.get("APP_DATABASE_USER", "endrex"),
        password=environ.get("APP_DATABASE_PASSWORD", "endrex"),
        database=environ.get("APP_DATABASE_NAME", "portal_api"),
        pool_size=int(environ.get("APP_DATABASE_POOL_SIZE", 20)),
        max_overflow=int(environ.get("APP_DATABASE_MAX_OVERFLOW", 20)),
    )


@pytest.fixture
def alembic_config(db_config: DatabaseConfig) -> AlembicConfig:
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options, pg_url=db_config.dsn)


@pytest.fixture
async def engine(db_config: DatabaseConfig) -> AsyncIterator[AsyncEngine]:
    async with create_engine(
        dsn=db_config.dsn,
        debug=False,
        pool_size=db_config.pool_size,
        pool_timeout=db_config.pool_timeout,
        max_overflow=db_config.max_overflow,
    ) as engine:
        async with engine.begin() as conn:
            await conn.run_sync(BaseTable.metadata.drop_all)
            await conn.run_sync(BaseTable.metadata.create_all)
        yield engine


@pytest.fixture
def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return create_sessionmaker(engine=engine)


@pytest.fixture
async def uow(session_factory: async_sessionmaker[AsyncSession]) -> SqlalchemyUow:
    return SqlalchemyUow(session_factory=session_factory)


@pytest.fixture
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
