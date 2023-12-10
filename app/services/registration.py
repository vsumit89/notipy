from app.repositories.registration.registration_repository import RegistrationRepository
from app.repositories.registration.registration_factory import (
    get_registration_repository,
)

from app.models.service_registration import ServiceRegistration
from app.models.exception import AppException

from utils.config import get_settings
from utils.string import generate_random_string


MAX_SERVICE_ID_LENGTH = 5
MAX_SERVICE_TOKEN_LENGTH = 26


class RegistrationService:
    """
    Registration service registers a service and returns a service_id and a service_token
    """

    def __init__(self) -> None:
        settings = get_settings()
        self.repository = get_registration_repository(settings.DB_STORE)

    async def create_service_token(self) -> ServiceRegistration:
        try:
            service_id = generate_random_string(MAX_SERVICE_ID_LENGTH)
            service_token = generate_random_string(MAX_SERVICE_TOKEN_LENGTH)

            registration = await self.repository.create_service_token(
                service_id, service_token
            )

            return registration
        except AppException as e:
            raise e

    async def validate_service_token(self, service_id, token) -> bool:
        try:
            return await self.repository.validate_service_token(service_id, token)
        except AppException as e:
            return False
