from abc import ABC, abstractmethod
from uuid import UUID


class IChatParticipantRepository(ABC):
    @abstractmethod
    async def is_chat_member(self, *, chat_id: UUID, user_id: UUID) -> bool: ...
