from app.repositories.event_manager.event_manager_repository import (
    EventManagerRepository,
)

from app.models.event_manager import Event
from app.models.channels import EmailChannel, ChannelType, SMSChannel

from app.dtos.event_manager import CreateEvent

from utils.logger import CustomLogger


class MongoEventManagerRepository(EventManagerRepository):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return

        self.__initialized = True
        self.logger = CustomLogger(__name__)

    async def get_event(self, id):
        pass
        # return await self.db_service.client.find_one({"_id": id})

    async def get_events(self):
        pass
        # return await self.db_service.client.find().to_list(1000)

    async def create_event(self, event: CreateEvent):
        try:
            channels = {}

            if "email" in event.channels:
                channels["email"] = EmailChannel(
                    no_of_attachments=event.channels["email"].no_of_attachments,
                    subject=event.channels["email"].subject,
                    content=event.channels["email"].content,
                    is_html=event.channels["email"].is_html,
                )

            if "sms" in event.channels:
                channels["sms"] = SMSChannel(
                    content=event.channels["sms"].content,
                )

            new_event = Event(
                name=event.name,
                description=event.description,
                channels=channels,
            )

            await new_event.insert()

            return new_event
        except Exception as e:
            self.logger.error("error in inserting document", str(e))

        # return await self.db_service.client.insert_one(event)

    async def update_event(self, id, event):
        pass
        # return await self.db_service.client.find_one_and_replace(
        #     {"_id": id}, event
        # )

    async def delete_event(self, id):
        pass
        # return await self.db_service.client.find_one_and_delete({"_id": id})
