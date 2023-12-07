from abc import ABC, abstractmethod


# EventManagerRepository is a singleton class that is used to run crud operations on the event_manager collection
class EventManagerRepository(ABC):
    def __init__(self):
        client = None

    @abstractmethod
    def get_event(self, id):
        pass

    @abstractmethod
    def get_events(self):
        pass

    @abstractmethod
    def create_event(self, event):
        pass

    @abstractmethod
    def update_event(self, id, event):
        pass

    @abstractmethod
    def delete_event(self, id):
        pass
