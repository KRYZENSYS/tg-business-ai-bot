"""User service: get-or-create, block, whitelist, list with pagination."""
from __future__ import annotations

from typing import List, Optional, Sequence

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserService:
    """All operations on the ``users`` table."""

    @staticmethod
    async def get(session: AsyncSession, telegram_id: int) -> Optional[User]:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_or_create(
        session: AsyncSession,
        telegram_id: int,
        username: Optional[str] = None,
        full_name: Optional[str] = None,
        language_code: Optional[str] = None,
    ) -> User:
        user = await UserService.get(session, telegram_id)
        if user is None:
            user = User(
                telegram_id=telegram_id,
                username=username,
                full_name=full_name,
                language_code=language_code or "uz",
            )
            session.add(user)
            await session.flush()
        else:
            user.last_seen = func.now()
            user.message_count = user.message_count + 1
            if username is not None:
                user.username = username
            if full_name is not None:
                user.full_name = full_name
        await session.commit()
        return user

    @staticmethod
    async def set_blocked(session: AsyncSession, telegram_id: int, blocked: bool) -> None:
        await session.execute(update(User).where(User.telegram_id == telegram_id).values(is_blocked=blocked))
        await session.commit()

    @staticmethod
    async def set_whitelisted(session: AsyncSession, telegram_id: int, value: bool) -> None:
        await session.execute(update(User).where(User.telegram_id == telegram_id).values(is_whitelisted=value))
        await session.commit()

    @staticmethod
    async def list_paginated(
        session: AsyncSession, page: int = 1, per_page: int = 10, search: Optional[str] = None
    ) -> tuple[Sequence[User], int]:
        stmt = select(User).order_by(User.last_seen.desc())
        if search:
            like = f"%{search.lower()}%"
            stmt = stmt.where(
                (User.username.ilike(like)) | (User.full_name.ilike(like)) | (User.telegram_id.cast(__import__("sqlalchemy").String).ilike(like))
            )
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await session.execute(count_stmt)).scalar_one()
        stmt = stmt.offset((page - 1) * per_page).limit(per_page)
        items = (await session.execute(stmt)).scalars().all()
        return items, total

    @staticmethod
    async def count(session: AsyncSession) -> int:
        return (await session.execute(select(func.count()).select_from(User))).scalar_one()
