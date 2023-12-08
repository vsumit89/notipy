from pydantic import BaseModel
from enum import Enum


class EmailChannel(BaseModel):
    subject: str
    is_html: bool
    content: str
    no_of_attachments: int


class SMSChannel(BaseModel):
    content: str


class ChannelType(Enum):
    EMAIL = "email"
    SMS = "sms"
