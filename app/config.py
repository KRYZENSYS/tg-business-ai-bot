"""Application configuration loaded from environment variables."""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Main application settings.

    All sensitive tokens and tunables are loaded from ``.env``.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Telegram
    bot_token: str = Field(..., alias="BOT_TOKEN")
    admin_id: int = Field(..., alias="ADMIN_ID")
    business_connection_id: str = Field(default="", alias="BUSINESS_CONNECTION_ID")

    # Database
    database_url: str = Field(default="sqlite+aiosqlite:///./data/bot.db", alias="DATABASE_URL")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    # AI
    groq_api_key: str = Field(..., alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_MODEL")
    ai_temperature: float = Field(default=0.7, alias="AI_TEMPERATURE")
    ai_max_tokens: int = Field(default=1024, alias="AI_MAX_TOKENS")
    ai_context_length: int = Field(default=20, alias="AI_CONTEXT_LENGTH")

    # Server
    webhook_host: str = Field(default="", alias="WEBHOOK_HOST")
    webhook_path: str = Field(default="/webhook", alias="WEBHOOK_PATH")
    webhook_port: int = Field(default=8080, alias="WEBHOOK_PORT")

    # Features
    auto_reply_enabled: bool = Field(default=True, alias="AUTO_REPLY_ENABLED")
    maintenance_mode: bool = Field(default=False, alias="MAINTENANCE_MODE")
    rate_limit_per_minute: int = Field(default=20, alias="RATE_LIMIT_PER_MINUTE")

    @property
    def webhook_url(self) -> str:
        return f"{self.webhook_host}{self.webhook_path}"


settings = Settings()
