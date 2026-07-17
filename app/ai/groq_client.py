"""Async Groq client with retries and timeouts."""
from __future__ import annotations

import asyncio
from typing import List, Optional

from groq import AsyncGroq
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings


class GroqClient:
    """Thin async wrapper around the official ``groq`` SDK."""

    def __init__(self) -> None:
        self._client: Optional[AsyncGroq] = None

    @property
    def client(self) -> AsyncGroq:
        if self._client is None:
            self._client = AsyncGroq(api_key=settings.groq_api_key, timeout=30.0)
        return self._client

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def chat(
        self,
        messages: List[dict],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> tuple[str, int]:
        """Call Groq chat completion, return (text, tokens_used)."""
        try:
            response = await self.client.chat.completions.create(
                model=model or settings.groq_model,
                messages=messages,
                temperature=temperature if temperature is not None else settings.ai_temperature,
                max_tokens=max_tokens or settings.ai_max_tokens,
                top_p=0.95,
                stream=False,
            )
            text = response.choices[0].message.content or ""
            tokens = response.usage.total_tokens if response.usage else 0
            return text.strip(), tokens
        except Exception as exc:
            logger.error(f"Groq API error: {exc}")
            raise


groq_client = GroqClient()
