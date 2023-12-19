from pydantic import BaseModel
from datetime import datetime


class EventDTO(BaseModel):
    name: str
    start_time: datetime
    team1: str
    team2: str
    location: str
    participants: int


class UserDTO(BaseModel):
    user_name: str
    email: str
    password: str # In db as hash
