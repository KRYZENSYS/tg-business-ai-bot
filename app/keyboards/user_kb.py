"""User-facing reply keyboard."""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def user_main_kb() -> ReplyKeyboardMarkup:
    """Return the main reply keyboard for ordinary users."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💬 Suhbat"), KeyboardButton(text="🔄 Yangilash")],
            [KeyboardButton(text="ℹ️ Yordam"), KeyboardButton(text="🌐 Til")],
        ],
        resize_keyboard=True,
    )
