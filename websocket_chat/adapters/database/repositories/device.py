from uuid import UUID

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from websocket_chat.adapters.database.tables import DeviceTable
from websocket_chat.adapters.database.uow import SqlalchemyUow
from websocket_chat.domain.interfaces.device_repository import IDeviceRepository


class PGDeviceRepository(IDeviceRepository):
    def __init__(self, *, uow: SqlalchemyUow) -> None:
        self.__uow = uow

    @property
    def __session(self) -> AsyncSession:
        return self.__uow.session

    async def create_or_update_device(self, *, device_id: UUID, user_id: UUID) -> None:
        stmt = (
            insert(DeviceTable)
            .values(
                id=device_id,
                user_id=user_id,
            )
            .on_conflict_do_update(
                index_elements=[DeviceTable.id],
                set_={
                    DeviceTable.last_seen_at: func.now(),
                },
            )
        )
        await self.__session.execute(stmt)
