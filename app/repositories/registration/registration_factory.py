from .registration_repository import RegistrationRepository

from database.mongodb.service_registration.registration import (
    MongoServiceRegistrationRepository,
)


def get_registration_repository(dbStore) -> RegistrationRepository:
    match dbStore:
        case "mongodb":
            return MongoServiceRegistrationRepository()
        case _:
            raise Exception("Database not supported")
