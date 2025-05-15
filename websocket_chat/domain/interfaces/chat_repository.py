from abc import ABC, abstractmethod
from uuid import UUID


class IChatRepository(ABC):
    @abstractmethod
    async def exists_by_id(self, *, chat_id: UUID) -> bool: ...
