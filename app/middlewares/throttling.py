"""ThrottlingMiddleware: simple in-memory rate limit (per minute)."""
from __future__ import annotations

import time
from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.config import settings
from app.utils.logger import logger


class ThrottlingMiddleware(BaseMiddleware):
    """Per-user rate limit using a sliding window of timestamps."""

    def __init__(self) -> None:
        self._hits: dict[int, list[float]] = defaultdict(list)
        self._limit = settings.rate_limit_per_minute
        self._window = 60.0

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is None:
            return await handler(event, data)
        now = time.time()
        bucket = self._hits[user.id]
        bucket[:] = [t for t in bucket if now - t < self._window]
        if len(bucket) >= self._limit:
            logger.warning(f"Rate limit hit: {user.id}")
            # We silently drop; the bot will respond with a friendly note elsewhere if needed.
            return None
        bucket.append(now)
        return await handler(event, data)
