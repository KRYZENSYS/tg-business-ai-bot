"""Background scheduler service for periodic tasks."""
from __future__ import annotations

import asyncio
from datetime import datetime

from aiogram import Bot
from loguru import logger

from app.services.statistics_service import StatisticsService


class SchedulerService:
    """Trivial background loop running once per hour."""

    def __init__(self) -> None:
        self._task: asyncio.Task | None = None

    async def _run(self, bot: Bot) -> None:
        while True:
            try:
                # Refresh cached daily stats here
                logger.debug("Scheduler tick @ %s", datetime.utcnow())
            except Exception as exc:  # pragma: no cover
                logger.error(f"Scheduler error: {exc}")
            await asyncio.sleep(3600)

    def start(self, bot: Bot) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._run(bot))

    def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            self._task = None


scheduler_service = SchedulerService()
