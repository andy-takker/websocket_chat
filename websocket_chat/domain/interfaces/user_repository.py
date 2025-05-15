from abc import ABC, abstractmethod
from uuid import UUID

from websocket_chat.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def fetch_user_by_email(self, *, email: str) -> User | None: ...

    @abstractmethod
    async def fetch_user_by_id(self, *, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def create_user(
        self, *, name: str, email: str, hashed_password: str
    ) -> User: ...
