from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from App.Dependencies import bl_factory
from DTO import EventDTO

events_api = APIRouter(
    prefix="/events",
    tags=["Event API"]
)


@events_api.get("")
def get_events(event_manager = Depends(bl_factory)):
    content, status_code = event_manager.get_events()
    return JSONResponse(status_code=status_code, content=content)


@events_api.get("/{event_id}")
def get_event_by_id(event_id: int, event_manager = Depends(bl_factory)):
    content, status_code = event_manager.get_event_by_id(event_id)
    return JSONResponse(status_code=status_code, content=content)


@events_api.delete("/{event_id}")
def delete_event(event_id: int, event_manager = Depends(bl_factory)):
    content, status_code = event_manager.delete_event_by_id(event_id)
    return JSONResponse(status_code=status_code, content=content)

@events_api.put("/{event_id}")
def update_event(event_id: int, event_data : dict = Body(), event_manager = Depends(bl_factory)):
    content, status_code = event_manager.update_event(event_id, event_data)
    return JSONResponse(status_code=status_code, content=content)


@events_api.post("")
def create_event(event_data : EventDTO = Body(), event_manager = Depends(bl_factory)):
    content, status_code = event_manager.create_event(event_data)
    return JSONResponse(status_code=status_code, content=content)


@events_api.get('/location/{event_location}')
def get_event_by_location(event_location: str, event_manager = Depends(bl_factory)):
    content, status_code = event_manager.get_event_by_location(event_location)
    return JSONResponse(status_code=status_code, content=content)

@events_api.get('/sort/{sort_key}')
def get_event_by_sort_key(sort_key: str, event_manager = Depends(bl_factory)):
    content, status_code = event_manager.get_event_by_sort_key(sort_key)
    return JSONResponse(status_code=status_code, content=content)
