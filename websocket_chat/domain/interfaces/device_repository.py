from abc import ABC, abstractmethod
from uuid import UUID


class IDeviceRepository(ABC):
    @abstractmethod
    async def create_or_update_device(self, *, device_id: UUID, user_id: UUID) -> None:
        raise NotImplementedError
