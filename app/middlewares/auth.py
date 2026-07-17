"""AuthMiddleware: blocks banned users and ensures user record exists."""
from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TGUser

from app.config import settings
from app.models.user import User
from app.services.user_service import UserService
from app.utils.logger import logger


class AuthMiddleware(BaseMiddleware):
    """Create/refresh the user record, and short-circuit if banned."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        tg_user: TGUser | None = data.get("event_from_user")
        session = data.get("session")
        if tg_user is None or session is None:
            return await handler(event, data)

        user: User = await UserService.get_or_create(
            session,
            telegram_id=tg_user.id,
            username=tg_user.username,
            full_name=tg_user.full_name,
            language_code=tg_user.language_code,
        )
        data["user"] = user

        # Admins are never blocked
        if tg_user.id != settings.admin_id and user.is_blocked:
            logger.info(f"Blocked user tried to interact: {tg_user.id}")
            return None
        return await handler(event, data)
