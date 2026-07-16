"""User model: stores Telegram user info and per-user state."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """Telegram user tracked by the bot."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    language_code: Mapped[Optional[str]] = mapped_column(String(8), default="uz", nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_whitelisted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_business: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    business_connection_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    first_seen: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    message_count: Mapped[int] = mapped_column(default=0, nullable=False)
