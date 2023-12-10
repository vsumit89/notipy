from pydantic import BaseModel


class ServiceTokenDTO(BaseModel):
    service_id: str
    service_token: str



