from datetime import datetime
from uuid import UUID

from sqlalchemy import ARRAY, Boolean, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from websocket_chat.adapters.database.base import (
    BaseTable,
    IdentifableMixin,
    TimestampedMixin,
    now_with_tz,
)


class UserTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)


class DeviceTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "devices"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user_agent: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    push_token: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )


class ChatTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "chats"

    title: Mapped[str | None] = mapped_column(String(255))
    is_group: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    creator_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class ChatParticipantTable(BaseTable):
    __tablename__ = "chat_participants"

    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        default=now_with_tz,
    )


class MessageTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "messages"

    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sender_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    text: Mapped[str] = mapped_column(String(1023), nullable=False)
    read_by: Mapped[list[UUID]] = mapped_column(
        ARRAY(PGUUID), nullable=False, default=list
    )
