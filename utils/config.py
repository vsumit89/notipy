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
    DB_HOST: str = "mongodb"
    DB_PORT: int = 27017
    DB_USERNAME: str = "root"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "notipy"
    DB_STORE: str = "mongodb"

    # CORS CONFIG VARIABLES
    CORS_ORIGINS: List[str] = ["*"]
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["Content-Type", "Authorization"]

    # MESSAGING QUEUE CONFIG VARIABLES
    MQ_HOST: str = "rabbitmq"
    MQ_PORT: int = 5672
    MQ_USERNAME: str = "rabbitmquser"
    MQ_PASSWORD: str = "rabbitmqpassword"
    MQ_VHOST: str = "notipy"

    # EMAIL SERVICE CONFIG VARIABLES
    EMAIL_SERVICE_API_URL = "EMAIL_SERVICE_API"
    EMAIL_DOMAIN = "EMAIL_DOMAIN"
    EMAIL_API_KEY = "EMAIL_API_KEY"
    EMAIL_NAME = "Sumit Vishwakarma"
    EMAIL_FROM = "vsumit030201@gmail.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
