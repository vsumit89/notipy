from app.repositories.event_manager.event_manager_factory import (
    get_event_manager_repository,
)
from app.dtos.event_manager import CreateEvent
from utils.logger import CustomLogger
from utils.config import get_settings


class EventManagerService:
    def __init__(self) -> None:
        settings = get_settings()
        self.repository = get_event_manager_repository(settings.DB_STORE)
        self.logger = CustomLogger(__name__)

    async def create_event(self, event: CreateEvent):
        try:
            new_event = await self.repository.create_event(event=event)
            return new_event
        except Exception as e:
            self.logger.error("error in creating an event", e)
            raise Exception
