from abc import ABC, abstractmethod
from app.models.service_registration import ServiceRegistration


class RegistrationRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def create_service_token(
        self, service_id: str, service_token: str
    ) -> ServiceRegistration:
        pass

    @abstractmethod
    async def validate_service_token(self, service_id, token) -> bool:
        pass
