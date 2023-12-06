from fastapi import APIRouter
from worker.send_notification import send_notifications

# events_manager_router is an APIRouter object which will be used to define all the routes related to events
events_manager_router = APIRouter()


# creates an event
@events_manager_router.post("/events")
async def create_event():
    """
    Create an event
    """
    return {"message": "event created"}


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
