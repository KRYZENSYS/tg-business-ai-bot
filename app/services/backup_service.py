"""Backup service: export/import database, snapshot files."""
from __future__ import annotations

import json
import os
import shutil
from datetime import datetime
from typing import List

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.backup import Backup
from app.models.base import Base


class BackupService:
    """File-based database backup / restore."""

    BACKUP_DIR = "backups"

    @staticmethod
    def ensure_dir() -> str:
        os.makedirs(BackupService.BACKUP_DIR, exist_ok=True)
        return BackupService.BACKUP_DIR

    @staticmethod
    async def create(session: AsyncSession, admin_id: int, note: str = "") -> Backup:
        BackupService.ensure_dir()
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{ts}.json"
        path = os.path.join(BackupService.BACKUP_DIR, filename)

        dump: dict = {}
        for table in Base.metadata.sorted_tables:
            rows = (await session.execute(select(table))).mappings().all()
            dump[table.name] = [dict(r) for r in rows]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(dump, f, default=str, ensure_ascii=False)

        size = os.path.getsize(path)
        record = Backup(filename=filename, size_bytes=size, created_by=admin_id, note=note)
        session.add(record)
        await session.commit()
        await session.refresh(record)
        logger.info(f"Backup created: {filename} ({size} bytes)")
        return record

    @staticmethod
    async def list_backups(session: AsyncSession) -> List[Backup]:
        from sqlalchemy import desc

        result = await session.execute(select(Backup).order_by(desc(Backup.created_at)))
        return list(result.scalars().all())

    @staticmethod
    async def restore(session: AsyncSession, filename: str) -> int:
        BackupService.ensure_dir()
        path = os.path.join(BackupService.BACKUP_DIR, filename)
        if not os.path.isfile(path):
            raise FileNotFoundError(filename)

        with open(path, "r", encoding="utf-8") as f:
            dump = json.load(f)

        # Wipe + reload
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        for table in Base.metadata.sorted_tables:
            for row in dump.get(table.name, []):
                await session.execute(table.insert().values(**row))
        await session.commit()
        logger.info(f"Backup restored: {filename}")
        return sum(len(v) for v in dump.values())
