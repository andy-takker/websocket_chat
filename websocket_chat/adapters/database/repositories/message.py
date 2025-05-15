from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from websocket_chat.adapters.database.tables import MessageTable
from websocket_chat.adapters.database.uow import SqlalchemyUow
from websocket_chat.domain.entities.chat import Message
from websocket_chat.domain.interfaces.message_repository import IMessageRepository


class PGMessageRepository(IMessageRepository):
    def __init__(self, *, uow: SqlalchemyUow) -> None:
        self.__uow = uow

    @property
    def __session(self) -> AsyncSession:
        return self.__uow.session

    async def count_chat_messages(self, *, chat_id: UUID) -> int:
        stmt = select(func.count(MessageTable.id)).where(
            MessageTable.chat_id == chat_id
        )
        return await self.__session.scalar(stmt) or 0

    async def fetch_chat_messages(
        self, *, chat_id: UUID, limit: int, offset: int
    ) -> Sequence[Message]:
        stmt = (
            select(MessageTable)
            .where(MessageTable.chat_id == chat_id)
            .limit(limit)
            .offset(offset)
        )

        result = await self.__session.scalars(stmt)
        return [
            Message(
                id=message.id,
                chat_id=message.chat_id,
                sender_id=message.sender_id,
                text=message.text,
                read_by=message.read_by,
                created_at=message.created_at,
            )
            for message in result
        ]
