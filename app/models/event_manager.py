from beanie import Document
from typing import Optional, Dict, Union
from datetime import datetime
from pydantic import Field


from app.models.channels import EmailChannel, SMSChannel, ChannelType


class Event(Document):
    created_at: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
    updated_at: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
    deleted_at: Optional[datetime] = None
    name: str
    description: str
    channels: Optional[Dict[str, Union[EmailChannel, SMSChannel]]] = None

    class Settings:
        collection = "events"
