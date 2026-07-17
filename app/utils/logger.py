"""Logger setup using loguru."""
from __future__ import annotations

import sys

from loguru import logger


def setup_logger() -> None:
    """Configure loguru for stdout + file output."""
    logger.remove()
    logger.add(sys.stdout, colorize=True, level="INFO", enqueue=True,
               format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")
    logger.add("logs/bot.log", rotation="10 MB", retention="14 days", level="DEBUG", enqueue=True, encoding="utf-8")
