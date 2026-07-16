"""Media record: stores metadata about files received from users."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Media(Base):
    """Metadata about media received from a user."""

    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), index=True, nullable=False)
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    file_unique_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    media_type: Mapped[str] = mapped_column(String(32), nullable=False)
    mime_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(nullable=True)
    caption: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    transcription: Mapped[Optional[str]] = mapped_column(String(4096), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
