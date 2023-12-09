from app.external.notifications.notification import NotificationService


class EmailNotificationService(NotificationService):
    def __init__(self, client_url, api_key):
        self.client_url = client_url
        self.api_key = api_key

    def send_notification(
        self,
    ):
        pass
