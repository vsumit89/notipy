from app.repositories.event_manager.event_manager_factory import (
    get_event_manager_repository,
)
from app.repositories.notification.notifications_factory import (
    get_notifications_repository,
)

from app.dtos.event_manager import CreateEvent, GetNotificationsResponse

from app.models.notifications import NotificationStatus, Notification
from app.models.exception import AppException

from app.services.notification_manager import NotificationManagerService

from utils.logger import CustomLogger
from utils.config import get_settings



class EventManagerService:
    def __init__(self) -> None:
        settings = get_settings()
        self.repository = get_event_manager_repository(settings.DB_STORE)
        self.logger = CustomLogger(__name__)
        self.notification_repository = get_notifications_repository(settings.DB_STORE)

    async def create_event(self, event: CreateEvent):
        try:
            new_event = await self.repository.create_event(event=event)
            return new_event
        except AppException as e:
            raise e

    async def get_events(self, limit, offset, query):
        try:
            event_details = await self.repository.get_events(limit, offset, query)
            return event_details
        except AppException as e:
            raise e

    async def get_event_by_id(self, id):
        try:
            event = await self.repository.get_event(id)
            return event
        except AppException as e:
            raise e

    async def update_event(self, id, event):
        try:
            updated_event = await self.repository.update_event(id, event)
            return updated_event
        except AppException as e:
            raise e

    async def delete_event(self, id):
        try:
            is_deleted = await self.repository.delete_event(id)
            return is_deleted
        except AppException as e:
            raise e

    async def initiate_notifications(self, event_id, dynamic_data):
        try:
            event = await self.repository.get_event(event_id)

            notification_manager = NotificationManagerService(event.channels)

            await notification_manager.validate_metadata(dynamic_data)

            await notification_manager.send_notifications(event_id, dynamic_data)

        except AppException as e:
            raise e

    async def get_notifications(
        self,
        event_id: str,
        limit: int,
        offset: int,
        status: NotificationStatus | None,
    ) -> GetNotificationsResponse:
        try:
            notification_details = await self.notification_repository.get_notifications(
                event_id=event_id, limit=limit, offset=offset, status=status
            )
            return notification_details
        except AppException as e:
            raise e

    async def get_notification(self, id) -> Notification:
        try:
            notification = await self.notification_repository.get_notification(id)
            return notification
        except AppException as e:
            self.logger.error("error in fetching notification")
            raise e
