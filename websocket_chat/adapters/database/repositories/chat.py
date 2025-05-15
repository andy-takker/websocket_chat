from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from websocket_chat.adapters.database.tables import ChatTable
from websocket_chat.adapters.database.uow import SqlalchemyUow
from websocket_chat.domain.interfaces.chat_repository import IChatRepository


class PGChatRepository(IChatRepository):
    def __init__(self, *, uow: SqlalchemyUow) -> None:
        self.__uow = uow

    @property
    def __session(self) -> AsyncSession:
        return self.__uow.session

    async def exists_by_id(self, *, chat_id: UUID) -> bool:
        stm = select(exists().where(ChatTable.id == chat_id))
        return bool(await self.__session.scalar(stm))
