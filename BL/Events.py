from datetime import datetime
import pytz
import sqlite3
from .DTO import EventDTO

class EventManager:
    def __init__(self, event_db):
        self.event_db = event_db

    def create_event(self, event: EventDTO):
        try:
            # Business logic: Schedule the event
            # Example: Check if date is in the future before scheduling
            insertion_time = pytz.utc.localize(datetime.now())
            if event.date > insertion_time:
                self.event_db.add_event(*list(event.__dict__.values()), creation_time=insertion_time)
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

    def get_event_by_id(self, event_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving event: {e}")

    def delete_event(self, event_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting event: {e}")

    def get_event_details(self, event_id):
        try:
            event = self.event_db.get_event_by_id(event_id)
            if event:
                return event
            else:
                return None
        except Exception as e:
            print(f"Error retrieving event details: {e}")
            return None

    # Other business logic methods for reminders, subscription management, etc.
