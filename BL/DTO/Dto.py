from pydantic import BaseModel
from datetime import datetime


class EventDTO(BaseModel):
    name: str
    start_time: datetime
    team1: str
    team2: str
    location: str
    participants: int