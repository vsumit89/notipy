from utils.logger import CustomLogger
from app.models.notifications import Notification, NotificationStatus
from app.repositories.notification.notifications_repository import (
    NotificationsRepository,
)
from app.dtos.event_manager import GetNotificationsResponse
from typing import List
from pymongo import DESCENDING


class MongoNotificationRepository(NotificationsRepository):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return

        self.__initialized = True
        self.logger = CustomLogger(__name__)

    async def create_notification(self, notification: Notification):
        try:
            new_notification = await Notification.insert(notification)
            return new_notification
        except Exception as e:
            print("this is the error")
            raise e

    async def update_notification_status(self, id, status: NotificationStatus):
        try:
            notification = await Notification.get(id)
            await notification.set({Notification.status: status})

        except Exception as e:
            raise e

    async def get_notifications(
        self, event_id, limit, offset, status
    ) -> GetNotificationsResponse:
        try:
            filter = {}
            if event_id:
                filter[Notification.event_id] = event_id
            if status:
                filter[Notification.status] = status

            count = await Notification.find(filter).count()

            notifications = (
                await Notification.find(filter)
                .sort([(Notification.created_at, DESCENDING)])
                .skip(offset)
                .limit(limit)
                .to_list()
            )
            return GetNotificationsResponse(total=count, notifications=notifications)
        except Exception as e:
            raise e

    async def get_notification(self, id) -> Notification:
        try:
            notification = await Notification.get(id)
            if notification is None:
                raise Exception("notification not found")
            return notification
        except Exception as e:
            raise e
