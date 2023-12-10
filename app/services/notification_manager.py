from typing import Dict, Any

from app.repositories.notification.notifications_factory import (
    get_notifications_repository,
)

from utils.config import get_settings
from utils.logger import CustomLogger

from app.validators.notification_validator import NotificationValidator

from app.models.notifications import Notification, NotificationStatus
from app.models.exception import AppException
from app.models.channels import EmailChannel, SMSChannel, ChannelType

from worker.send_notification import send_notifications


class NotificationManagerService:
    """
    NotificationManagerService class is responsible for validating the metadata sent with the event
    and then sending the notifications to the respective channels
    Validations in metadata (Email):
    1. To email address should be present
    2. The dynamic data in the email template should be present in the metadata
    Validations in metadata (SMS):
    1. To phone number should be present
    2. The dynamic data in the SMS template should be present in the metadata
    """

    def __init__(self, channels: Dict[str, EmailChannel | SMSChannel]) -> None:
        self.channels = channels
        self.logger = CustomLogger(__name__)
        settings = get_settings()
        self.repository = get_notifications_repository(settings.DB_STORE)

    async def validate_metadata(self, dynamic_data: Dict[str, Any]) -> bool:
        """
        Validates the metadata sent with the event
        :param metadata: metadata sent with the event
        :return: True if the metadata is valid else False
        """
        try:
            for channel_type, channel_data in self.channels.items():
                if channel_type == ChannelType.EMAIL.value:
                    NotificationValidator.validate(
                        ChannelType.EMAIL,
                        channel_data,
                        dynamic_data[ChannelType.EMAIL.value],
                    )
                elif channel_type == ChannelType.SMS.value:
                    NotificationValidator.validate(
                        ChannelType.SMS,
                        channel_data,
                        dynamic_data[ChannelType.SMS.value],
                    )
        except AppException as e:
            raise e

    async def _send_email_notification(
        self, event_id, channel_data: EmailChannel, dynamic_data: Dict[str, str]
    ):
        try:
            notification = await self.repository.create_notification(
                Notification(
                    event_id=event_id,
                    channel_type=ChannelType.EMAIL,
                    dynamic_data=dynamic_data,
                    status=NotificationStatus.INITIATED,
                )
            )

            send_notifications.apply_async(
                args=[
                    str(notification.id),
                    ChannelType.EMAIL.value,
                    channel_data.__dict__,
                    dynamic_data,
                ]
            )
        except AppException as e:
            raise e

    async def _send_sms_notification(
        self, event_id, channel_data: SMSChannel, dynamic_data
    ):
        pass

    async def send_notifications(self, event_id, dynamic_data: Dict[str, str]):
        """
        Puts the notification task in the queue and updates the status of the event
        in the database
        :param dynamic_data: dynamic data sent with the event
        """
        try:
            for channel_type, channel_data in self.channels.items():
                if channel_type == ChannelType.EMAIL.value:
                    await self._send_email_notification(
                        event_id, channel_data, dynamic_data[ChannelType.EMAIL.value]
                    )
                elif channel_type == ChannelType.SMS.value:
                    await self._send_sms_notification(
                        event_id, channel_data, dynamic_data[ChannelType.SMS.value]
                    )
        except AppException as e:
            raise e
