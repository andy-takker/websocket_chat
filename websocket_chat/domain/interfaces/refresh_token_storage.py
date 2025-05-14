from abc import ABC, abstractmethod
from uuid import UUID


class IRefreshTokenStorage(ABC):
    @abstractmethod
    async def save_refresh_token(
        self,
        *,
        device_id: UUID,
        token: str,
    ) -> None: ...

    @abstractmethod
    async def get_refresh_token(
        self,
        *,
        device_id: UUID,
    ) -> str | None: ...

    @abstractmethod
    async def del_refresh_token(
        self,
        *,
        device_id: UUID,
    ) -> None: ...

    @abstractmethod
    async def del_all_refresh_tokens(
        self,
        *,
        user_id: UUID,
    ) -> None: ...
