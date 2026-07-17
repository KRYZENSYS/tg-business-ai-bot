"""Async Redis wrapper used for FSM, throttling, and runtime config."""
from __future__ import annotations

from typing import Optional

import redis.asyncio as redis
from loguru import logger

from app.config import settings


class RedisService:
    """Thin wrapper around the async redis client."""

    def __init__(self) -> None:
        self._client: Optional[redis.Redis] = None

    @property
    def redis(self) -> Optional[redis.Redis]:
        return self._client

    async def connect(self) -> None:
        """Try to connect; if it fails we still work in memory."""
        try:
            self._client = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
            )
            await self._client.ping()
            logger.info("Redis connected")
        except Exception as exc:
            logger.warning(f"Redis unavailable, falling back to memory: {exc}")
            self._client = None

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            logger.info("Redis closed")


redis_service = RedisService()
