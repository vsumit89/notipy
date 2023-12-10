from fastapi import HTTPException, Request, status
from app.services.registration import RegistrationService


async def validate_service_token(
    request: Request,
):
    try:
        registration_service = RegistrationService()

        service_id = request.headers["X-Service-Id"]
        service_token = request.headers["X-Service-Token"]

        if not await registration_service.validate_service_token(
            service_id, service_token
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid service_id or service_token",
            )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service_id or service_token",
        )


async def token_middleware(request: Request, call_next):
    if request.url.path == "/api/v1/register":
        return await call_next(request)
    await validate_service_token(request=request)
    return await call_next(request)
