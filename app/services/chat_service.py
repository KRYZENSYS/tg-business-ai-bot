"""Chat history service: append, fetch, clear conversation messages."""
from __future__ import annotations

from typing import List, Optional, Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import ChatMessage


class ChatService:
    """Operations on per-user AI conversation history."""

    @staticmethod
    async def add_message(
        session: AsyncSession,
        user_id: int,
        role: str,
        content: str,
        detected_language: Optional[str] = None,
        tokens_used: int = 0,
    ) -> ChatMessage:
        msg = ChatMessage(
            user_id=user_id,
            role=role,
            content=content,
            detected_language=detected_language,
            tokens_used=tokens_used,
        )
        session.add(msg)
        await session.commit()
        await session.refresh(msg)
        return msg

    @staticmethod
    async def get_recent(session: AsyncSession, user_id: int, limit: int = 20) -> Sequence[ChatMessage]:
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        items = list(result.scalars().all())
        items.reverse()  # chronological order
        return items

    @staticmethod
    async def clear_history(session: AsyncSession, user_id: int) -> int:
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount or 0
