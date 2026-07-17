"""Setting service: read/write dynamic runtime configuration."""
from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.setting import Setting


class SettingService:
    """Key-value runtime config (prompt, model, temperature, …)."""

    @staticmethod
    async def get(session: AsyncSession, key: str, default: Optional[str] = None) -> Optional[str]:
        result = await session.execute(select(Setting).where(Setting.key == key))
        s = result.scalar_one_or_none()
        return s.value if s else default

    @staticmethod
    async def set(session: AsyncSession, key: str, value: str) -> None:
        result = await session.execute(select(Setting).where(Setting.key == key))
        s = result.scalar_one_or_none()
        if s:
            s.value = value
        else:
            session.add(Setting(key=key, value=value))
        await session.commit()

    @staticmethod
    async def get_int(session: AsyncSession, key: str, default: int = 0) -> int:
        v = await SettingService.get(session, key)
        try:
            return int(v) if v is not None else default
        except (TypeError, ValueError):
            return default

    @staticmethod
    async def get_float(session: AsyncSession, key: str, default: float = 0.0) -> float:
        v = await SettingService.get(session, key)
        try:
            return float(v) if v is not None else default
        except (TypeError, ValueError):
            return default

    @staticmethod
    async def get_bool(session: AsyncSession, key: str, default: bool = False) -> bool:
        v = await SettingService.get(session, key)
        if v is None:
            return default
        return v.lower() in ("1", "true", "yes", "on")
