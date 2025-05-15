from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MessageModel(BaseModel):
    id: UUID
    chat_id: UUID
    sender_id: UUID
    text: str
    read_by: Sequence[UUID]
    created_at: datetime


class ChatHistoryResponseModel(BaseModel):
    messages: Sequence[MessageModel]
    total: int
