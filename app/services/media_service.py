"""Media service: persist and list media metadata."""
from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.media import Media


class MediaService:
    """CRUD for media history records."""

    @staticmethod
    async def record(
        session: AsyncSession,
        user_id: int,
        file_id: str,
        media_type: str,
        file_unique_id: Optional[str] = None,
        mime_type: Optional[str] = None,
        file_size: Optional[int] = None,
        caption: Optional[str] = None,
        transcription: Optional[str] = None,
    ) -> Media:
        m = Media(
            user_id=user_id,
            file_id=file_id,
            file_unique_id=file_unique_id,
            media_type=media_type,
            mime_type=mime_type,
            file_size=file_size,
            caption=caption,
            transcription=transcription,
        )
        session.add(m)
        await session.commit()
        await session.refresh(m)
        return m

    @staticmethod
    async def list_for_user(session: AsyncSession, user_id: int, limit: int = 50) -> Sequence[Media]:
        stmt = select(Media).where(Media.user_id == user_id).order_by(desc(Media.created_at)).limit(limit)
        return (await session.execute(stmt)).scalars().all()

    @staticmethod
    async def set_transcription(session: AsyncSession, media_id: int, text: str) -> None:
        from sqlalchemy import update

        await session.execute(update(Media).where(Media.id == media_id).values(transcription=text))
        await session.commit()
