from app.external.notifications.email import EmailNotificationService
from notifications.sms import SMSNotificationService


def get_notification_service(type):
    match type:
        case "email":
            return EmailNotificationService()
        case "sms":
            return SMSNotificationService()
        case _:
            raise Exception("Invalid notification type")
