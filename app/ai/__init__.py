"""AI subpackage: Groq client, prompt builder, language detection."""
from app.ai.groq_client import GroqClient, groq_client
from app.ai.prompts import BASE_PROMPT, build_messages
from app.ai.lang_detect import detect_language

__all__ = ["GroqClient", "groq_client", "BASE_PROMPT", "build_messages", "detect_language"]
