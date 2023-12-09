from typing import Dict

from app.models.channels import EmailChannel, SMSChannel


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

    def validate_metadata(self, metadata: Dict[str, str]) -> bool:
        """
        Validates the metadata sent with the event
        :param metadata: metadata sent with the event
        :return: True if the metadata is valid else False
        """
