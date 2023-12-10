from app.repositories.registration.registration_repository import RegistrationRepository


from app.models.service_registration import ServiceRegistration
from app.models.exception import AppException


class MongoServiceRegistrationRepository(RegistrationRepository):
    async def create_service_token(
        self, service_id: str, service_token: str
    ) -> ServiceRegistration:
        registration = ServiceRegistration(
            service_id=service_id, service_token=service_token
        )

        await registration.insert()
        return registration

    async def validate_service_token(self, service_id, token) -> bool:
        try:
            query = ServiceRegistration.find(
                {ServiceRegistration.service_id: service_id}
            )

            registration = await query.first_or_none()
            if registration is None:
                return False

            if registration.service_token == token:
                return True

            return False
        except AppException as e:
            return False
