from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    """
    Settings class stores the config variables for the service
    """

    # PROJECT CONFIG VARIABLES
    PROJECT_NAME: str = "NotiPy"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "A multichannel notification service"
    PROJECT_DOCS_URL: str = "/docs"

    # DATABASE CONFIG VARIABLES

    # CORS CONFIG VARIABLES
    CORS_ORIGINS: List[str] = ["*"]
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["Content-Type", "Authorization"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True