"""BlockedFilter: pass for users in the blocked list (used in admin menus)."""
from __future__ import annotations

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from app.database.engine import async_session_factory
from app.models.user import User


class BlockedFilter(BaseFilter):
    """True if the sender is currently in the blocked users list."""

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        if not event.from_user:
            return False
        async with async_session_factory() as s:
            res = await s.execute(select(User).where(User.telegram_id == event.from_user.id))
            u = res.scalar_one_or_none()
            return bool(u and u.is_blocked)
