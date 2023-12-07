from app.repositories.event_manager.event_manager_factory import (
    get_event_manager_repository,
)

from utils.logger import CustomLogger
from utils.config import get_settings


class EventManagerService:
    def __init__(self) -> None:
        settings = get_settings()
        self.repository = get_event_manager_repository(settings.DB_STORE)
        self.logger = CustomLogger(__name__)

    async def create_event(self):
        try:
            await self.repository.create_event()
        except Exception as e:
            self.logger.error("error in creating an event", e)
