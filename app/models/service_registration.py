from beanie import Document


class ServiceRegistration(Document):
    service_id: str
    service_token: str
