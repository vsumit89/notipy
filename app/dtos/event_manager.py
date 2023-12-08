from pydantic import BaseModel
from typing import Dict, Union, Optional
from app.models.channels import EmailChannel, SMSChannel
from app.models.event_manager import Event


class CreateEvent(BaseModel):
    name: str
    description: str
    channels: Optional[Dict[str, Union[EmailChannel, SMSChannel]]] = None


class CreateEventResponse(BaseModel):
    event: Optional[Event]
    message: str
