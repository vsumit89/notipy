from jinja2 import Environment, BaseLoader, TemplateSyntaxError, Template
import re

from app.models.channels import ChannelType, EmailChannel, SMSChannel


class NotificationValidator:
    """
    NotificationValidator class is responsible for validating the dynamic data sent with the event
    """

    TO_EMAIL_NOT_PRESENT = Exception("to_email is required")
    NUMBER_OF_ATTACHMENTS_MISMATCH = Exception("Number of attachments mismatch")

    @staticmethod
    def validate(channel_type, channel_data, dynamic_data):
        match channel_type:
            case ChannelType.EMAIL:
                return NotificationValidator._validate_email(channel_data, dynamic_data)
            case ChannelType.SMS:
                return NotificationValidator._validate_sms(channel_data, dynamic_data)
            case _:
                raise Exception("Invalid notification type")

    @staticmethod
    def _validate_email(channel_data: EmailChannel, dynamic_data):
        if not dynamic_data["to_email"]:
            raise NotificationValidator.TO_EMAIL_NOT_PRESENT

        if channel_data.no_of_attachments != len(dynamic_data["attachments"]):
            raise NotificationValidator.NUMBER_OF_ATTACHMENTS_MISMATCH

        if channel_data.is_html:
            template_env = Environment(loader=BaseLoader())
            try:
                template = template_env.from_string(channel_data.content)
                template.placeholders = set(
                    re.findall(r"{{\s*(\w+)\s*}}", channel_data.content)
                )
            except TemplateSyntaxError:
                template.placeholders = set()

            missing_fields = template.placeholders - set(dynamic_data.metadata.keys())
            if missing_fields:
                raise Exception(
                    f"Missing fields in metadata: {', '.join(missing_fields)}"
                )
        else:
            template = Template(channel_data.content)
            missing_fields = [
                key for key in template.keys() if key not in dynamic_data.metadata
            ]

            if missing_fields:
                raise Exception(
                    f"Missing fields in metadata: {', '.join(missing_fields)}"
                )

        return True

    @staticmethod
    def _validate_sms(channel_data: SMSChannel, dynamic_data):
        if not channel_data.to_phone_number:
            return False
        if not channel_data.content:
            return False
        if not dynamic_data:
            return False
        return True
