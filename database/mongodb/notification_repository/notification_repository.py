from utils.logger import CustomLogger
from app.models.notifications import Notification, NotificationStatus
from app.repositories.notification.notifications_repository import (
    NotificationsRepository,
)
from app.dtos.event_manager import GetNotificationsResponse
from app.models.exception import AppException
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
        except AppException as e:
            raise e

    async def get_notification(self, id) -> Notification:
        try:
            notification = await Notification.get(id)
            if notification is None:
                raise AppException(
                    status_code=404,
                    message="notification not found",
                    detail="notification_id provided is not valid. Please try again with a valid notification_id",
                )
            return notification
        except ValueError as e:
            raise AppException(
                status_code=422,
                message="notification_id provided is not valid",
                detail="notification_id provided is not valid. Please try again with a valid notification_id",
            )
        except AppException as e:
            raise e
