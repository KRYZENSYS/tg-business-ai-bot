"""AdminFilter: only the configured admin id passes."""
from __future__ import annotations

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from app.config import settings


class AdminFilter(BaseFilter):
    """Pass for users whose id matches ``settings.admin_id``."""

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return bool(event.from_user and event.from_user.id == settings.admin_id)
