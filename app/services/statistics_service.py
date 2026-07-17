"""Statistics service: per-day counter aggregation."""
from __future__ import annotations

from datetime import date

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.statistics import Statistics
from app.models.user import User


class StatisticsService:
    """Daily dashboard counters."""

    @staticmethod
    async def bump(session: AsyncSession, **kwargs: int) -> None:
        today = date.today()
        result = await session.execute(select(Statistics).where(Statistics.day == today))
        row = result.scalar_one_or_none()
        if row is None:
            row = Statistics(day=today, **kwargs)
            session.add(row)
        else:
            for k, v in kwargs.items():
                setattr(row, k, getattr(row, k, 0) + v)
        await session.commit()

    @staticmethod
    async def total_users(session: AsyncSession) -> int:
        return (await session.execute(select(func.count()).select_from(User))).scalar_one()

    @staticmethod
    async def blocked(session: AsyncSession) -> int:
        return (
            await session.execute(select(func.count()).select_from(User).where(User.is_blocked.is_(True)))
        ).scalar_one()

    @staticmethod
    async def recent_days(session: AsyncSession, days: int = 7) -> Sequence[Statistics]:
        stmt = select(Statistics).order_by(desc(Statistics.day)).limit(days)
        return (await session.execute(stmt)).scalars().all()
