from .notifications_repository import NotificationsRepository
from database.mongodb.notification_repository.notification_repository import (
    MongoNotificationRepository,
)


def get_notifications_repository(dbStore) -> NotificationsRepository:
    match dbStore:
        case "mongodb":
            return MongoNotificationRepository()
        case _:
            raise Exception("Database not supported")
