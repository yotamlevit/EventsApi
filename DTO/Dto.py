from pydantic import BaseModel
from datetime import datetime

class EventDTO(BaseModel):
    name: str
    date: datetime
    team1: str
    team2: str
    location: str
    participants: int