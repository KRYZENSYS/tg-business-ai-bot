"""Lightweight language detection for Uzbek, Russian, English."""
from __future__ import annotations

import re
from typing import Optional

# Cyrillic letters (Russian, Uzbek Cyrillic)
_CYRILLIC = re.compile(r"[\u0400-\u04FF]")
# Latin script with Uzbek/English specific markers
_LATIN = re.compile(r"[A-Za-z]")


def detect_language(text: str) -> str:
    """Return ISO-639-1 code ('uz', 'ru', 'en') for the given text."""
    if not text:
        return "uz"
    cyr = len(_CYRILLIC.findall(text))
    lat = len(_LATIN.findall(text))

    text_lower = text.lower()

    if cyr > lat:
        # Could be Russian or Uzbek (Cyrillic)
        # Uzbek Cyrillic contains Ÿ (ҳ, ғ, қ, Ҳ, Ғ, Қ) or ў
        if any(ch in text_lower for ch in ("\u049b", "\u04b3", "\u0493", "\u04af", "\u04bb", "\u04e3")):
            return "uz"
        return "ru"

    if lat > 0:
        # Latin: distinguish English from Uzbek (with x, o', g', sh, ch)
        if any(comb in text_lower for comb in ("o'", "g'", "sh", "ch", "ng")):
            return "uz"
        # Heuristic: short common English words
        if re.search(r"\b(the|is|are|was|have|will|hello|hi|thanks)\b", text_lower):
            return "en"
        # Default for Latin script in our bot's audience
        return "uz"

    return "uz"
