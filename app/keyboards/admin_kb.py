"""Admin inline keyboards."""
from __future__ import annotations

from typing import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_main_kb() -> InlineKeyboardMarkup:
    """Return the main admin dashboard keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Statistika", callback_data="adm:stats"),
             InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="adm:users:1")],
            [InlineKeyboardButton(text="📢 Broadcast", callback_data="adm:broadcast"),
             InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="adm:settings")],
            [InlineKeyboardButton(text="🤖 AI", callback_data="adm:ai"),
             InlineKeyboardButton(text="🛠 Texnik", callback_data="adm:tech")],
            [InlineKeyboardButton(text="💾 Backup", callback_data="adm:backup"),
             InlineKeyboardButton(text="🚫 Bloklar", callback_data="adm:blocked")],
            [InlineKeyboardButton(text="📜 Loglar", callback_data="adm:logs"),
             InlineKeyboardButton(text="🔍 Qidirish", callback_data="adm:search")],
        ]
    )


def stats_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Yangilash", callback_data="adm:stats"),
             InlineKeyboardButton(text="⬅️ Orqaga", callback_data="adm:home")],
        ]
    )


def users_kb(page: int, has_next: bool) -> InlineKeyboardMarkup:
    rows = []
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"adm:users:{page-1}"))
    nav.append(InlineKeyboardButton(text=f"📄 {page}", callback_data="adm:noop"))
    if has_next:
        nav.append(InlineKeyboardButton(text="➡️", callback_data=f"adm:users:{page+1}"))
    rows.append(nav)
    rows.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="adm:home")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def pagination_kb(prefix: str, page: int, has_next: bool) -> InlineKeyboardMarkup:
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"{prefix}:{page-1}"))
    if has_next:
        nav.append(InlineKeyboardButton(text="➡️", callback_data=f"{prefix}:{page+1}"))
    return InlineKeyboardMarkup(inline_keyboard=[nav, [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="adm:home")]])


def settings_kb(auto_reply: bool, ai_enabled: bool, maintenance: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🔁 Auto-reply: {'✅' if auto_reply else '❌'}", callback_data="adm:toggle:auto_reply")],
            [InlineKeyboardButton(text=f"🧠 AI: {'✅' if ai_enabled else '❌'}", callback_data="adm:toggle:ai")],
            [InlineKeyboardButton(text=f"🛠 Maintenance: {'✅' if maintenance else '❌'}", callback_data="adm:toggle:maintenance")],
            [InlineKeyboardButton(text="✏️ Prompt", callback_data="adm:set:prompt"),
             InlineKeyboardButton(text="🔢 Max tokens", callback_data="adm:set:tokens")],
            [InlineKeyboardButton(text="🌡 Temperature", callback_data="adm:set:temp"),
             InlineKeyboardButton(text="📏 Kontekst", callback_data="adm:set:ctx")],
            [InlineKeyboardButton(text="🧠 Model", callback_data="adm:set:model"),
             InlineKeyboardButton(text="🔑 API key", callback_data="adm:set:apikey")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="adm:home")],
        ]
    )


def backup_kb(backups: Sequence) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text="➕ Yangi backup", callback_data="adm:backup:create")]]
    for b in backups[:5]:
        rows.append([InlineKeyboardButton(text=f"📦 {b.filename}", callback_data=f"adm:backup:restore:{b.id}")])
    rows.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="adm:home")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def broadcast_confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Yuborish", callback_data="adm:bc:yes"),
             InlineKeyboardButton(text="❌ Bekor", callback_data="adm:bc:no")],
        ]
    )
