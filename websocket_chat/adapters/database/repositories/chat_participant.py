from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from websocket_chat.adapters.database.tables import ChatParticipantTable
from websocket_chat.adapters.database.uow import SqlalchemyUow
from websocket_chat.domain.interfaces.chat_participant_repository import (
    IChatParticipantRepository,
)


class PGChatParticipantRepository(IChatParticipantRepository):
    def __init__(self, *, uow: SqlalchemyUow) -> None:
        self.__uow = uow

    @property
    def __session(self) -> AsyncSession:
        return self.__uow.session

    async def is_chat_member(self, *, chat_id: UUID, user_id: UUID) -> bool:
        stmt = select(
            exists().where(
                ChatParticipantTable.chat_id == chat_id,
                ChatParticipantTable.user_id == user_id,
            )
        )
        return bool(await self.__session.scalar(stmt))
