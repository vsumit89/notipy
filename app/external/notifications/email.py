import requests
from pydantic import BaseModel
from jinja2 import BaseLoader, Environment, Template

from typing import List
from .notification import NotificationService
from utils.config import get_settings


class EmailData(BaseModel):
    to_email: List[str]
    subject: str
    is_html: bool
    content: str


class EmailNotificationService(NotificationService):
    def __init__(self):
        pass

    def render_template(self, static_text: str, dynamic_data: dict, is_html: bool):
        if is_html:
            template_env = Environment(loader=BaseLoader())
            template = template_env.from_string(static_text)
            return template.render(dynamic_data)
        else:
            template = Template(static_text)
            return template.render(dynamic_data)

    def send_notification(self, email_data: EmailData) -> bool:
        try:
            settings = get_settings()

            url = f"{settings.EMAIL_SERVICE_API_URL}/{settings.EMAIL_DOMAIN}/messages"

            data = {
                "from": f"{settings.EMAIL_NAME} <{settings.EMAIL_FROM}>",
                "to": email_data.to_email,
                "subject": email_data.subject,
            }

            if email_data.is_html:
                data["html"] = email_data.content
            else:
                data["text"] = email_data.content

            data = requests.post(
                url=url,
                auth=("api", settings.EMAIL_API_KEY),
                data=data,
            )

            if data.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False
