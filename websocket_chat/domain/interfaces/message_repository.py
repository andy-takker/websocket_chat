from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from websocket_chat.domain.entities.chat import Message


class IMessageRepository(ABC):
    @abstractmethod
    async def fetch_chat_messages(
        self, *, chat_id: UUID, limit: int, offset: int
    ) -> Sequence[Message]: ...

    @abstractmethod
    async def count_chat_messages(self, *, chat_id: UUID) -> int: ...
