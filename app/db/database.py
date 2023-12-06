from abc import ABC, abstractmethod


class DatabaseService(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def migrate(self):
        pass
