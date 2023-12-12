from pydantic import BaseModel
from datetime import datetime

class EventDTO(BaseModel):
    id: int
    name: str
    date: datetime
    team1: str
    team2: str
    location: str
    participants: int