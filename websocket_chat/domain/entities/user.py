from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, kw_only=True, slots=True)
class UserRegister:
    name: str
    email: str
    password: str
    device_id: UUID


@dataclass(frozen=True, kw_only=True, slots=True)
class User:
    id: UUID
    name: str
    email: str
