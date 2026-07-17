"""Spam detection: naive but effective filter."""
from __future__ import annotations

import re
from collections import Counter

# Quick blocklist of common spam words (uz/ru/en)
_BAD = re.compile(
    r"\b(viagra|sex|porn|kazino|казино|ставки|заработок|реклама|спам|reklama|spam)\b",
    re.IGNORECASE,
)
_URL = re.compile(r"https?://\S+|t\.me/\S+|@\w+", re.IGNORECASE)


def is_spam(text: str) -> bool:
    """Return True if the message looks like spam."""
    if not text:
        return False
    if _BAD.search(text):
        return True
    urls = _URL.findall(text)
    if len(urls) >= 3:
        return True
    # Same character repeated 25+ times
    if any(count > 25 for _, count in Counter(text).items()):
        return True
    return False
