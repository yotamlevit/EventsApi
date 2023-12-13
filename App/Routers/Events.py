from fastapi import APIRouter, Depends, Body
from App.Dependencies import bl_factory
from BL.DTO import EventDTO

events_api = APIRouter(
    prefix="/events",
    tags=["Event API"]
)


@events_api.get("")
def get_events(event_manager = Depends(bl_factory)):
    return event_manager.get_events()


@events_api.get("/{event_id}")
def get_event(event_id: str, event_manager = Depends(bl_factory)):
    return event_manager.get_event(event_id)


@events_api.delete("/{event_id}")
def delete_event(event_id: str, event_manager = Depends(bl_factory)):
    return event_manager.delete_event_by_id(event_id)

@events_api.put("/{event_id}")
def update_event(event_id: str, event_data : dict = Body(), event_manager = Depends(bl_factory)):
    return event_manager.update_event(event_id, event_data)


@events_api.post("")
def create_event(event_data : EventDTO = Body(), event_manager = Depends(bl_factory)):
    return event_manager.create_event(event_data)


@events_api.get('/location/{event_location}')
def get_event_by_location(event_location, event_manager = Depends(bl_factory)):
    return event_manager.get_event_by_location(event_location)

@events_api.get('/sort/{sort_key}')
def get_event_by_sort_key(sort_key, event_manager = Depends(bl_factory)):
    return event_manager.get_event_by_sort_key(sort_key)

@events_api.get("/{event_name}")
def get_event_by_name(event_name: str, event_manager = Depends(bl_factory)):
    pass

@events_api.delete("/name/{event_name}")
def delete_event_by_name(event_name: str, event_manager = Depends(bl_factory)):
    pass