from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, kw_only=True, slots=True)
class TokenPair:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, kw_only=True, slots=True)
class TokenPayload:
    user_id: UUID
    device_id: UUID


@dataclass(frozen=True, kw_only=True, slots=True)
class RefreshIn:
    refresh_token: str
