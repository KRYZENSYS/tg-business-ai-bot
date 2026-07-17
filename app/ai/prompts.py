"""System prompts and message-builder helpers."""
from __future__ import annotations

from typing import Iterable, List

BASE_PROMPT = (
    "Siz samimiy, qisqa va foydali AI yordamchisiz. "
    "Foydalanuvchi yozgan tilda (o'zbek, rus yoki ingliz) javob bering. "
    "Javoblaringiz qisqa, samimiy va kontekstga mos bo'lsin. "
    "Keraksiz uzun matn yozmang. Emoji va kichik pauzalar ishlatishingiz mumkin."
)


def build_messages(
    history: Iterable,  # Iterable[ChatMessage]
    new_user_text: str,
    system_prompt: str = BASE_PROMPT,
) -> List[dict]:
    """Convert DB history + new user message into the OpenAI/Groq message format."""
    messages: List[dict] = [{"role": "system", "content": system_prompt}]
    for h in history:
        role = h.role
        if role not in ("user", "assistant", "system"):
            continue
        messages.append({"role": role, "content": h.content})
    messages.append({"role": "user", "content": new_user_text})
    return messages
