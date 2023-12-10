from abc import ABC

from app.dtos.event_manager import GetNotificationsResponse


# NotificationsRepository is a singleton class that is used to run crud operations on the notifications collection
class NotificationsRepository(ABC):
    def __init__(self):
        pass

    async def create_notification(self, notification):
        pass

    async def update_notification_status(self, id, status):
        pass

    async def get_notifications(
        self, event_id, limit, offset, status
    ) -> GetNotificationsResponse:
        pass

    async def get_notification(self, id):
        pass
