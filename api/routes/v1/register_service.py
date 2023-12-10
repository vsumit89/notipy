from fastapi import APIRouter, Depends, Response

from app.services.registration import RegistrationService
from app.models.exception import AppException, AppExceptionResponse
from app.models.service_registration import ServiceRegistration

registration_router = APIRouter()


@registration_router.post("/register", response_model=ServiceRegistration)
async def register_user(
    response: Response,
    registration_service: RegistrationService = Depends(),
):
    """
    Registers a service and returns a service_id and a service_token
    """

    try:
        registration = await registration_service.create_service_token()
        return registration
    except AppException as e:
        response.status_code = e.status_code
        return AppExceptionResponse(message=e.message, detail=e.detail)
