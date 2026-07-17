"""Aiogram middlewares: logging, throttling, auth, session injection."""
from aiogram import Dispatcher

from app.middlewares.auth import AuthMiddleware
from app.middlewares.session_mw import SessionMiddleware
from app.middlewares.throttling import ThrottlingMiddleware


def register_all_middlewares(dp: Dispatcher) -> None:
    """Wire all middlewares to the dispatcher."""
    # Session + Auth run for every message
    dp.message.middleware(SessionMiddleware())
    dp.callback_query.middleware(SessionMiddleware())
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())


__all__ = ["register_all_middlewares", "SessionMiddleware", "AuthMiddleware", "ThrottlingMiddleware"]
