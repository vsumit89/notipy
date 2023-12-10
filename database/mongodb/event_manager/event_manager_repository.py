from datetime import datetime
from typing import Dict

from app.repositories.event_manager.event_manager_repository import (
    EventManagerRepository,
)

from app.models.event_manager import Event
from app.models.channels import EmailChannel, SMSChannel
from app.models.exception import AppException
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
        try:
            event = await Event.get(id)
            if event is None or event.deleted_at is not None:
                raise AppException(
                    status_code=404,
                    message="event not found",
                    detail="event_id provided is not valid. Please try again with a valid event_id",
                )
            return event
        except AppException as e:
            raise e

    # get_events returns a list of events and the total count based on the limit, offset and query
    async def get_events(self, limit, offset, query):
        try:
            if query == None:
                total_count = await Event.find({"deleted_at": None}).count()
                events = (
                    await Event.find({"deleted_at": None})
                    .skip(offset)
                    .limit(limit)
                    .to_list()
                )
                return {
                    "total_count": total_count,
                    "events": events,
                }
            else:
                filter_query = {
                    "$and": [
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"description": {"$regex": query, "$options": "i"}},
                            ]
                        },
                        {
                            "deleted_at": None
                        },  # Added this condition to filter out soft-deleted events
                    ]
                }

                query = Event.find(filter_query)
                total_count = await query.count()

                events = await query.skip(offset).limit(limit).to_list()
                return {
                    "total_count": total_count,
                    "events": events,
                }
        except AppException as e:
            raise e

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
        except AppException as e:
            self.logger.error("error in inserting document", str(e))
            raise e

        # return await self.db_service.client.insert_one(event)

    async def update_event(self, id, event: CreateEvent):
        try:
            old_event = await Event.get(id)

            if event.name is not None:
                old_event.name = event.name

            if event.description is not None:
                old_event.description = event.description

            channels: Dict[str, EmailChannel | SMSChannel] = {}

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

            updated_event = await old_event.set(
                {
                    Event.name: old_event.name,
                    Event.description: old_event.description,
                    Event.channels: channels,
                }
            )

            return updated_event
        except AppException as e:
            raise e

    async def delete_event(self, id):
        try:
            event = await Event.get(id)
            if event.deleted_at is not None:
                raise Exception("event not found")

            await event.set({Event.deleted_at: int(datetime.utcnow().timestamp())})
            return True

        except AppException as e:
            self.logger.error("error in deleting document", str(e))
            raise e
