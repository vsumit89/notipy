from fastapi import APIRouter, Depends, Response

from worker.send_notification import send_notifications
from app.services.event_manager import EventManagerService
from app.dtos.event_manager import CreateEvent, CreateEventResponse

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
async def get_events():
    """
    Get all events
    """
    send_notifications.apply_async()
    return {"message": "all events fetched"}


@events_manager_router.get("/events/{event_id}")
async def get_event(event_id: int):
    """
    Get an event
    """
    return {"message": f"event {event_id} fetched"}


@events_manager_router.put("/events/{event_id}")
async def update_event(event_id: int):
    """
    Update an event
    """
    return {"message": f"event {event_id} updated"}


@events_manager_router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    """
    Delete an event
    """
    return {"message": f"event {event_id} deleted"}
