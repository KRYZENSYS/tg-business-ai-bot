"""Admin service: audit log, listing, helpers."""
from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin_log import AdminLog


class AdminService:
    """Audit trail for every privileged action."""

    @staticmethod
    async def log(
        session: AsyncSession,
        admin_id: int,
        action: str,
        target_id: Optional[int] = None,
        details: Optional[str] = None,
    ) -> None:
        entry = AdminLog(admin_id=admin_id, action=action, target_id=target_id, details=details)
        session.add(entry)
        await session.commit()

    @staticmethod
    async def list_recent(session: AsyncSession, limit: int = 50) -> Sequence[AdminLog]:
        stmt = select(AdminLog).order_by(desc(AdminLog.created_at)).limit(limit)
        return (await session.execute(stmt)).scalars().all()
