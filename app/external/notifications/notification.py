from abc import ABC, abstractmethod


class NotificationService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def send_notification(self, notification):
        pass
