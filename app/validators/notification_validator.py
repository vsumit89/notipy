from jinja2 import Environment, BaseLoader, TemplateSyntaxError, meta
import re

from app.models.channels import ChannelType, EmailChannel, SMSChannel


class NotificationValidator:
    """
    NotificationValidator class is responsible for validating the dynamic data sent with the event
    """

    TO_EMAIL_NOT_PRESENT = Exception("to_email is required")
    NUMBER_OF_ATTACHMENTS_MISMATCH = Exception("Number of attachments mismatch")

    @staticmethod
    def validate(channel_type: ChannelType, channel_data, dynamic_data):
        match channel_type:
            case ChannelType.EMAIL:
                return NotificationValidator._validate_email(channel_data, dynamic_data)
            case ChannelType.SMS:
                return NotificationValidator._validate_sms(channel_data, dynamic_data)
            case _:
                raise Exception("Invalid notification type")

    @staticmethod
    def _validate_email(channel_data: EmailChannel, dynamic_data):
        try:
            if "to_email" not in dynamic_data or not dynamic_data["to_email"]:
                raise NotificationValidator.TO_EMAIL_NOT_PRESENT

            if "attachments" in dynamic_data:
                if len(dynamic_data["attachments"]) != channel_data.no_of_attachments:
                    raise NotificationValidator.NUMBER_OF_ATTACHMENTS_MISMATCH
            else:
                if channel_data.no_of_attachments != 0:
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

                if "metadata" not in dynamic_data and len(template.placeholders) > 0:
                    raise Exception("metadata is required")

                missing_fields = template.placeholders - set(
                    dynamic_data["metadata"].keys()
                )
                if missing_fields:
                    raise Exception(
                        f"Missing fields in metadata: {', '.join(missing_fields)}"
                    )
            else:
                env = Environment()
                # Parse the template to extract variable names
                parsed_content = env.parse(channel_data.content)
                template_variables = meta.find_undeclared_variables(parsed_content)

                missing_fields = [
                    variable
                    for variable in template_variables
                    if variable not in dynamic_data["metadata"]
                ]

                if missing_fields:
                    raise Exception(
                        f"Missing fields in metadata: {', '.join(missing_fields)}"
                    )

        except Exception as e:
            raise e

    @staticmethod
    def _validate_sms(channel_data: SMSChannel, dynamic_data):
        if not channel_data.to_phone_number:
            return False
        if not channel_data.content:
            return False
        if not dynamic_data:
            return False
        return True
