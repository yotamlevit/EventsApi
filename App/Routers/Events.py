from fastapi import APIRouter, Depends, Body
from App.Dependencies import authenticate
from BL.DTO import EventDTO
from BL.Events import EventManager


from DL.EventDB import EventDB
event_db = EventDB()

# Create an instance of EventManager
event_manager = EventManager(event_db)
events_api = APIRouter(
    prefix="/events",
    tags=["Event API"]
)


@events_api.get("")
def get_events(auth = Depends(authenticate)):
    pass


@events_api.get("/{event_name}")
def get_event(event_name: str, auth = Depends(authenticate)):
    pass

@events_api.delete("/{event_name}")
def delete_event(event_name: str):
    pass


@events_api.delete("/{event_id}")
def delete_event(event_id: str):
    pass

@events_api.put("/{event_name}")
def update_event(event_name: str, event_data : EventDTO = Body()):
    pass


@events_api.post("")
def create_event(event_data : EventDTO = Body()):
    event_manager.create_event(event_data)