from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, kw_only=True, slots=True)
class FetchChatHistory:
    chat_id: UUID
    limit: int
    offset: int


@dataclass(frozen=True, kw_only=True, slots=True)
class Message:
    id: UUID
    chat_id: UUID
    sender_id: UUID
    text: str
    read_by: Sequence[UUID]
    created_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class ChatHistory:
    chat_id: UUID
    total: int
    messages: Sequence[Message]
