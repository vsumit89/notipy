from database.mongodb.event_manager.event_manager_repository import (
    MongoEventManagerRepository,
)
from .event_manager_repository import EventManagerRepository


def get_event_manager_repository(dbStore) -> EventManagerRepository:
    match dbStore:
        case "mongodb":
            return MongoEventManagerRepository()
        case _:
            raise Exception("Database not supported")
