from beanie import Document
from enum import Enum
from datetime import datetime
from pydantic import Field

from app.models.channels import ChannelType


class NotificationStatus(Enum):
    INITIATED = "initiated"
    SUCCESS = "success"
    FAILED = "failed"


class Notification(Document):
    created_at: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
    channel_type: ChannelType
    event_id: str
    dynamic_data: dict
    status: NotificationStatus

    class Settings:
        collection = "notifications"
