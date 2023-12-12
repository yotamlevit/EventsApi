from fastapi import APIRouter, Depends, Body


events_api = APIRouter(
    prefix="/events",
    tags=["Event API"]
)


@events_api.get()
def get_events():
    pass


@events_api.get("/{event_name}")
def get_event(event_name: str):
    pass

@events_api.delete("/{event_name}")
def delete_event(event_name: str):
    pass

@events_api.put("/{event_name}")
def update_event(event_name: str, event_data : dict = Body()):
    pass


@events_api.post("/{event_name}")
def create_event(event_name: str, event_data : dict = Body()):
    pass