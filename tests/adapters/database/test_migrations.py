from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from tests.utils import get_diff_db_metadata, run_async_migrations
from websocket_chat.adapters.database.tables import BaseTable


async def test_migrations_up_to_date(alembic_config, engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.drop_all)
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
    await run_async_migrations(alembic_config, BaseTable.metadata, "head")
    async with engine.connect() as connection:
        diff = await connection.run_sync(
            get_diff_db_metadata,
            metadata=(BaseTable.metadata,),
        )
    assert not diff
