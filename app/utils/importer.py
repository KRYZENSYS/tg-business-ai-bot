"""Database import (restore from JSON)."""
from __future__ import annotations

import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base


async def import_db(session: AsyncSession, path: str) -> int:
    """Wipe and reload from a JSON dump produced by ``export_db``."""
    with open(path, "r", encoding="utf-8") as f:
        dump = json.load(f)
    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(table.delete())
    for table in Base.metadata.sorted_tables:
        for row in dump.get(table.name, []):
            await session.execute(table.insert().values(**row))
    await session.commit()
    return sum(len(v) for v in dump.values())
