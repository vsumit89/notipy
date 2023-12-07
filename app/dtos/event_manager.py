from pydantic import BaseModel
from typing import Dict, Any


class CreateEvent(BaseModel):
    name: str
    description: str
    channels: Dict[str, Any]
