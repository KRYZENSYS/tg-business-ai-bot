"""Application entry point: wires bot, FastAPI webhook server, scheduler."""
from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
from loguru import logger

from app.config import settings
from app.database.engine import close_db, init_db
from app.handlers import register_all_handlers
from app.middlewares import register_all_middlewares
from app.services.redis_service import redis_service
from app.utils.logger import setup_logger


async def on_startup(bot: Bot) -> None:
    """Hook called when bot is started: set webhook, init DB."""
    await init_db()
    if settings.webhook_host:
        await bot.set_webhook(
            url=settings.webhook_url,
            allowed_updates=["message", "business_message", "business_connection", "callback_query"],
            drop_pending_updates=True,
        )
        logger.info(f"Webhook set: {settings.webhook_url}")
    logger.info("Bot started")


async def on_shutdown(bot: Bot) -> None:
    """Hook called when bot is shutting down: close connections."""
    await close_db()
    await redis_service.close()
    logger.info("Bot stopped")


async def main() -> None:
    """Application bootstrap."""
    setup_logger()

    storage = RedisStorage(redis_service.redis) if redis_service.redis else MemoryStorage()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    register_all_middlewares(dp)
    register_all_handlers(dp)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    if settings.webhook_host:
        app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=settings.webhook_path)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host="0.0.0.0", port=settings.webhook_port)
        await site.start()
        logger.info(f"Webhook server listening on port {settings.webhook_port}")
        try:
            await asyncio.Event().wait()
        finally:
            await runner.cleanup()
    else:
        await dp.start_polling(bot, allowed_updates=["message", "business_message", "callback_query"])


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user")
