from pydantic import BaseModel
from typing import Optional


class AppException(Exception):
    def __init__(
        self,
        message: str = "Internal server error",
        status_code: int = 500,
        detail: Optional[str] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail


class AppExceptionResponse(BaseModel):
    message: str
    detail: Optional[str] = None
