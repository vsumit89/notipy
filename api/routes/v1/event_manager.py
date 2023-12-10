from fastapi import APIRouter, Depends, Response
from typing import Dict, Any

from app.services.event_manager import EventManagerService
from app.dtos.event_manager import (
    CreateEvent,
    CreateEventResponse,
    GetNotificationsResponse,
)
from app.models.notifications import NotificationStatus, Notification

# events_manager_router is an APIRouter object which will be used to define all the routes related to events
events_manager_router = APIRouter()


# creates an event
@events_manager_router.post(
    "/events", response_model=CreateEventResponse, response_model_exclude_none=True
)
async def create_event(
    requestBody: CreateEvent,
    response: Response,
    event_service: EventManagerService = Depends(),
):
    """
    Creates an event
    """
    try:
        new_event = await event_service.create_event(requestBody)
        response_body = CreateEventResponse(
            event=new_event, message="event created successfully"
        )
        return response_body
    except Exception as e:
        response.status_code = 500
        response_body = CreateEventResponse(message=str(e), event=None)
        return response_body


@events_manager_router.get("/events")
async def get_events(
    response: Response,
    limit: int = 20,
    offset: int = 0,
    query: str = None,
    event_service: EventManagerService = Depends(),
):
    """
    Get all events
    """
    try:
        event_details = await event_service.get_events(limit, offset, query)
        return event_details
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}


@events_manager_router.get("/events/{event_id}")
async def get_event(
    response: Response,
    event_id: str,
    event_service: EventManagerService = Depends(),
):
    """
    Get an event
    """
    try:
        event = await event_service.get_event_by_id(event_id)
        return event
    except Exception as e:
        if str(e) == "event not found":
            response.status_code = 404
        else:
            response.status_code = 500
        return {"message": f"{str(e)}"}


@events_manager_router.put("/events/{event_id}")
async def update_event(
    request_body: CreateEvent,
    response: Response,
    event_id: str,
    event_service: EventManagerService = Depends(),
):
    """
    Update an event
    """
    try:
        updated_event = await event_service.update_event(event_id, request_body)
        return updated_event
    except:
        response.status_code = 500
        return {"message": f"unable to update event {event_id}"}


@events_manager_router.delete("/events/{event_id}")
async def delete_event(
    response: Response, event_id: str, event_service: EventManagerService = Depends()
):
    """
    Delete an event
    """
    try:
        is_deleted = await event_service.delete_event(event_id)
        if is_deleted:
            return {"message": f"event deleted successfully"}
        else:
            raise Exception("unable to delete event")
    except Exception as e:
        if str(e) == "event not found":
            response.status_code = 404
        else:
            response.status_code = 500
        return {"message": f"{str(e)}"}


@events_manager_router.post("/events/{event_id}/send_notifications")
async def send_notifications(
    requestBody: Dict[str, Any],
    response: Response,
    event_id: str,
    event_service: EventManagerService = Depends(),
):
    """
    Publish an event
    """
    try:
        await event_service.initiate_notifications(event_id, requestBody)
        return {"message": "notification has been queued successfully for delivery"}
    except Exception as e:
        response.status_code = 422
        return {"message": f"{str(e)}"}


@events_manager_router.get(
    "/events/{event_id}/get_notifications", response_model=GetNotificationsResponse
)
async def get_notifications(
    response: Response,
    event_id: str,
    limit: int = 20,
    offset: int = 0,
    status: NotificationStatus = None,
    event_service: EventManagerService = Depends(),
):
    """
    Get all notifications for an event
    """
    try:
        notifications = await event_service.get_notifications(
            event_id=event_id,
            limit=limit,
            offset=offset,
            status=status,
        )
        return notifications
    except Exception as e:
        response.status_code = 500
        return {"message": f"{str(e)}"}


@events_manager_router.get(
    "/notifications/{notification_id}", response_model=Notification | Dict[str, Any]
)
async def get_notification(
    response: Response,
    notification_id: str,
    event_service: EventManagerService = Depends(),
):
    """
    Get a notification for an event
    """
    try:
        notification = await event_service.get_notification(notification_id)
        return notification
    except Exception as e:
        if str(e) == "notification not found":
            response.status_code = 404
        else:
            response.status_code = 500
        return {"message": f"Internal server error"}
