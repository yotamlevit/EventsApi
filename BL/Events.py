from datetime import datetime
import pytz
import sqlite3
from .DTO import EventDTO
from DL import EventRepo

class EventManager:
    def __init__(self):
        self.events_repo = EventRepo()


    def get_events(self):
        return self.events_repo.get_events()

    def get_event(self, event_id):
        try:
            event = self.events_repo.get_event_by_id(event_id)
            if event:
                return event
            else:
                return None
        except Exception as e:
            print(f"Error retrieving event details: {e}")
            return None

    def get_event_by_location(self, event_location):
        try:
            event = self.events_repo.get_event_by_location(event_location)
            if event:
                return event
            else:
                return None
        except Exception as e:
            print(f"Error retrieving event details: {e}")
            return None

    def get_event_by_sort_key(self, sort_key):
        try:
            event = self.events_repo.get_event_by_sort_key(sort_key)
            if event:
                return event
            else:
                return None
        except Exception as e:
            print(f"Error retrieving event details: {e}")
            return None

    def create_event(self, event: EventDTO):
        try:
            insertion_time = pytz.utc.localize(datetime.now())
            if event.date > insertion_time:
                self.events_repo.create_event(event, insertion_time=insertion_time)
                return True
            else:
                return False
        except ValueError as e:
            print(f"Error scheduling event: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error adding event: {e}")
        except Exception as e:
            print(f"Unexpected error scheduling event: {e}")
            return False

    def update_event(self, event_id: int, updated_fields: dict):
        updated_fields['insertion_time'] = 'asdasda'#str(pytz.utc.localize(datetime.now()))
        return self.events_repo.update_event(event_id, updated_fields)

    def delete_event_by_id(self, event_id: str):
        # Delegate the deletion operation to the EventDB instance
        try:
            self.events_repo.delete_event(event_id)
            return True  # Return True if deletion is successful
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False  # Return False if an error occurs during deletion


    # Other business logic methods for reminders, subscription management, etc.
