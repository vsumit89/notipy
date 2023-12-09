from abc import ABC, abstractmethod


# NotificationsRepository is a singleton class that is used to run crud operations on the notifications collection
class NotificationsRepository(ABC):
    def __init__(self):
        pass

    async def create_notification(self, notification):
        pass

    async def update_notification_status(self, id, status):
        pass
