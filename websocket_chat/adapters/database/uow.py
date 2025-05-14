import asyncio
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncSessionTransaction,
    async_sessionmaker,
)

from websocket_chat.domain.uow import AbstractUow


class SqlalchemyUow(AbstractUow):
    session_factory: async_sessionmaker[AsyncSession]
    transaction: AsyncSessionTransaction | None
    __session: AsyncSession | None

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory
        self.__session = None
        self.transaction = None

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
        self.transaction = None

    async def create_transaction(self) -> None:
        if self.__session is not None:
            return None
        self.__session = self.session_factory()
        self.transaction = await self.session.begin()

    async def close_transaction(self, *exc: Any) -> None:
        task = asyncio.create_task(self.session.close())
        await asyncio.shield(task)

    @property
    def session(self) -> AsyncSession:
        if self.__session is None:
            raise ValueError("Session is not created")
        return self.__session
