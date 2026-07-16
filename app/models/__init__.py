"""Import all models so SQLAlchemy registers them on Base.metadata."""
from app.models.admin_log import AdminLog
from app.models.backup import Backup
from app.models.base import Base
from app.models.chat import ChatMessage
from app.models.log import Log
from app.models.media import Media
from app.models.setting import Setting
from app.models.statistics import Statistics
from app.models.user import User

__all__ = [
    "AdminLog",
    "Backup",
    "Base",
    "ChatMessage",
    "Log",
    "Media",
    "Setting",
    "Statistics",
    "User",
]
