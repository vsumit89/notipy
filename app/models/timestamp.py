from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Base(BaseModel):
    created_at: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
    updated_at: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
    deleted_at: Optional[datetime] = None
