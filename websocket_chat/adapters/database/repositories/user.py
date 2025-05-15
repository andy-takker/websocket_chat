from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from websocket_chat.adapters.database.tables import UserTable
from websocket_chat.adapters.database.uow import SqlalchemyUow
from websocket_chat.domain.entities.user import User
from websocket_chat.domain.interfaces.user_repository import IUserRepository


class PGUserRepository(IUserRepository):
    def __init__(self, *, uow: SqlalchemyUow) -> None:
        self.__uow = uow

    @property
    def __session(self) -> AsyncSession:
        return self.__uow.session

    async def fetch_user_by_email(self, *, email: str) -> User | None:
        stmt = select(UserTable).where(UserTable.email == email.lower())
        result = await self.__session.scalar(stmt)
        if result is None:
            return None
        return User(
            id=result.id,
            name=result.name,
            email=result.email,
            hashed_password=result.hashed_password,
        )

    async def fetch_user_by_id(self, *, user_id: UUID) -> User | None:
        stmt = select(UserTable).where(UserTable.id == user_id)
        result = await self.__session.scalar(stmt)
        if result is None:
            return None
        return User(
            id=result.id,
            name=result.name,
            email=result.email,
            hashed_password=result.hashed_password,
        )

    async def create_user(self, *, name: str, email: str, hashed_password: str) -> User:
        stmt = (
            insert(UserTable)
            .values(name=name, email=email.lower(), hashed_password=hashed_password)
            .returning(UserTable)
        )
        result = (await self.__session.scalars(stmt)).one()
        return User(
            id=result.id,
            name=result.name,
            email=result.email,
            hashed_password=result.hashed_password,
        )
