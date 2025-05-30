"""Initial migration

Revision ID: fc4047144c90
Revises:
Create Date: 2025-05-14 23:24:28.836013

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "fc4047144c90"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__users")),
        sa.UniqueConstraint("email", name=op.f("uq__users__email")),
    )
    op.create_table(
        "chats",
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("is_group", sa.Boolean(), nullable=False),
        sa.Column("creator_id", sa.UUID(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["users.id"],
            name=op.f("fk__chats__creator_id__users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__chats")),
    )
    op.create_table(
        "devices",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("push_token", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk__devices__user_id__users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__devices")),
    )
    op.create_index(op.f("ix__devices__user_id"), "devices", ["user_id"], unique=False)
    op.create_table(
        "chat_participants",
        sa.Column("chat_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["chat_id"],
            ["chats.id"],
            name=op.f("fk__chat_participants__chat_id__chats"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk__chat_participants__user_id__users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "chat_id", "user_id", name=op.f("pk__chat_participants")
        ),
    )
    op.create_index(
        op.f("ix__chat_participants__user_id"),
        "chat_participants",
        ["user_id"],
        unique=False,
    )
    op.create_table(
        "messages",
        sa.Column("chat_id", sa.UUID(), nullable=False),
        sa.Column("sender_id", sa.UUID(), nullable=False),
        sa.Column("text", sa.String(length=1023), nullable=False),
        sa.Column("read_by", sa.ARRAY(sa.UUID()), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["chat_id"],
            ["chats.id"],
            name=op.f("fk__messages__chat_id__chats"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["sender_id"],
            ["users.id"],
            name=op.f("fk__messages__sender_id__users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__messages")),
    )
    op.create_index(
        op.f("ix__messages__chat_id"), "messages", ["chat_id"], unique=False
    )
    op.create_index(
        op.f("ix__messages__sender_id"), "messages", ["sender_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix__messages__sender_id"), table_name="messages")
    op.drop_index(op.f("ix__messages__chat_id"), table_name="messages")
    op.drop_table("messages")
    op.drop_index(
        op.f("ix__chat_participants__user_id"), table_name="chat_participants"
    )
    op.drop_table("chat_participants")
    op.drop_index(op.f("ix__devices__user_id"), table_name="devices")
    op.drop_table("devices")
    op.drop_table("chats")
    op.drop_table("users")
    # ### end Alembic commands ###
