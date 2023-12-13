from datetime import datetime
from typing import Tuple

import pytz
import sqlite3
from .DTO import EventDTO, EventDTO
from DL import EventRepo
from http import HTTPStatus

class EventManager:
    def __init__(self):
        self.events_repo = EventRepo()

    def get_events(self) -> Tuple[dict, HTTPStatus]:
        try:
            events = self.events_repo.get_events()
            if events:
                events = [self.__parse_event(event) for event in events]
                return events, HTTPStatus.OK
            else:
                return {"message": "There are no events at the moment"}, HTTPStatus.NOT_FOUND
        except Exception as e:
            print(f"Error retrieving event details: {e}")
            return None, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_event(self, event_id: str) -> Tuple[dict, HTTPStatus]:
        try:
            event = self.events_repo.get_event_by_id(event_id)
            if event:
                return self.__parse_event(event[0]), HTTPStatus.OK
            else:
                return {"message": "Event id={} not found".format(event_id)}, HTTPStatus.NOT_FOUND
        except Exception as e:
            print(f"Error retrieving event details: {e}")
            return None, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_event_by_location(self, event_location) -> Tuple[dict, HTTPStatus]:
        try:
            events = self.events_repo.get_event_by_location(event_location)
            if events:
                events = [self.__parse_event(event) for event in events]
                return events, HTTPStatus.OK
            else:
                return {"message": "Events location={} not found".format(event_location)}, HTTPStatus.NOT_FOUND
        except Exception as e:
            print(f"Error retrieving event details: {e}")
            return None, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_event_by_sort_key(self, sort_key) -> Tuple[dict, HTTPStatus]:
        try:
            events = self.events_repo.get_event_by_sort_key(sort_key)
            if events:
                events = [self.__parse_event(event) for event in events]
                return events, HTTPStatus.OK
            else:
                return {"message": "There are no events at the moment"}, HTTPStatus.NOT_FOUND
        except Exception as e:
            print(f"Error retrieving event details: {e}")
            return None, HTTPStatus.INTERNAL_SERVER_ERROR

    def create_event(self, event: EventDTO) -> Tuple[dict, HTTPStatus]:
        try:
            insertion_time = pytz.utc.localize(datetime.now())
            if event.date > insertion_time:
                self.events_repo.create_event(event, insertion_time=insertion_time)
                return True, HTTPStatus.OK
            else:
                return False, HTTPStatus.BAD_REQUEST
        except ValueError as e:
            print(f"Error scheduling event: {e}")
            return False, HTTPStatus.BAD_REQUEST
        except sqlite3.Error as e:
            print(f"Error adding event: {e}")
        except Exception as e:
            print(f"Unexpected error scheduling event: {e}")
            return False, HTTPStatus.INTERNAL_SERVER_ERROR

    def update_event(self, event_id: int, updated_fields: dict) -> Tuple[dict, HTTPStatus]:
        updated_fields['insertion_time'] = 'asdasda'#str(pytz.utc.localize(datetime.now()))
        return self.events_repo.update_event(event_id, updated_fields)

    def delete_event_by_id(self, event_id: str) -> Tuple[dict, HTTPStatus]:
        # Delegate the deletion operation to the EventDB instance
        try:
            self.events_repo.delete_event(event_id)
            return True, HTTPStatus.OK  # Return True if deletion is successful
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False, HTTPStatus.INTERNAL_SERVER_ERROR  # Return False if an error occurs during deletion

    def __parse_event(self, event_data: list) -> dict:
        return {
            'id': event_data[0],
            'name': event_data[1],
            'date': event_data[2],
            'team1': event_data[3],
            'team2': event_data[4],
            'location': event_data[5],
            'creation_time': event_data[6]
        }
