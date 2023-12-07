from abc import ABC, abstractmethod


class DatabaseService(ABC):
    def __init__(self):
        client = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def migrate(self):
        pass
