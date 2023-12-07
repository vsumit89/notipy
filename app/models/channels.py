from pydantic import BaseModel
from typing import Optional


class EmailChannel(BaseModel):
    subject: str
    is_html: bool
    content: str
    no_of_attachments: int


class SMSChannel(BaseModel):
    content: str


class Channels(BaseModel):
    email: Optional[EmailChannel]
