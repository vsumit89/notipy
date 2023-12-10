from pydantic import BaseModel
from typing import Dict, Union, Optional, List
from app.models.channels import EmailChannel, SMSChannel
from app.models.event_manager import Event
from app.models.notifications import Notification


class CreateEvent(BaseModel):
    name: str
    description: str
    channels: Optional[Dict[str, Union[EmailChannel, SMSChannel]]] = None


class CreateEventResponse(BaseModel):
    event: Optional[Event]
    message: str


class GetNotificationsResponse(BaseModel):
    total: int
    notifications: List[Notification]
