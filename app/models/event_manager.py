from beanie import Document
from app.models.channels import EmailChannel, SMSChannel, ChannelType
from typing import Optional, Dict, Union
from .timestamp import Base


class Event(Document, Base):
    name: str
    description: str
    channels: Optional[Dict[str, Union[EmailChannel, SMSChannel]]] = None

    class Settings:
        collection = "events"
