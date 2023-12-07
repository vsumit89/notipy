from beanie import Document
from app.models.channels import Channels, EmailChannel, SMSChannel
from typing import Optional, Dict, Union


class Event(Document):
    name: str
    description: str
    channels: Optional[Dict[str, Union[EmailChannel, SMSChannel]]] = None

    class Settings:
        collection = "events"
