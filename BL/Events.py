from datetime import datetime
from typing import Tuple
import pytz
from http import HTTPStatus
from .DTO import EventDTO
from DL import EventRepo

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
        except Exception as err:
            return {"message": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_event_by_id(self, event_id: str) -> Tuple[dict, HTTPStatus]:
        try:
            event = self.events_repo.get_event_by_id(event_id)
            if event:
                return self.__parse_event(event[0]), HTTPStatus.OK
            else:
                return {"message": "Event id={} not found".format(event_id)}, HTTPStatus.NOT_FOUND
        except Exception as err:
            return {"message": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_event_by_location(self, event_location) -> Tuple[dict, HTTPStatus]:
        try:
            events = self.events_repo.get_event_by_location(event_location)
            if events:
                events = [self.__parse_event(event) for event in events]
                return events, HTTPStatus.OK
            else:
                return {"message": "Events location={} not found".format(event_location)}, HTTPStatus.NOT_FOUND
        except Exception as err:
            return {"message": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_event_by_sort_key(self, sort_key) -> Tuple[dict, HTTPStatus]:
        try:
            events = self.events_repo.get_event_by_sort_key(sort_key)
            if events:
                events = [self.__parse_event(event) for event in events]
                return events, HTTPStatus.OK
            else:
                return {"message": "There are no events at the moment"}, HTTPStatus.NOT_FOUND
        except ValueError as value_err:
            return {"message": str(value_err)}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {"message": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def create_event(self, event: EventDTO) -> Tuple[dict, HTTPStatus]:
        try:
            insertion_time = pytz.utc.localize(datetime.now())
            if event.date > insertion_time:
                self.events_repo.create_event(event, insertion_time=insertion_time)
                return True, HTTPStatus.OK
            else:
                return {"message": f"Error scheduling event: event time has already past"}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {"message": str(err), "event_data": event.__dict__}, HTTPStatus.INTERNAL_SERVER_ERROR

    def update_event(self, event_id: int, updated_fields: dict) -> Tuple[dict, HTTPStatus]:
        try:
            _, status_code = self.get_event_by_id(event_id)
            if status_code != HTTPStatus.OK:
                raise ValueError(f"Event with id {event_id} does not exist")

            updated_fields['insertion_time'] = 'asdasda'#str(pytz.utc.localize(datetime.now()))
            return self.events_repo.update_event(event_id, updated_fields), HTTPStatus.OK
        except ValueError as value_err:
            return {"message": str(value_err), "event_data": {"id": event_id, "update_fields": updated_fields}}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {"message": str(err), "event_data": {"id": event_id, "update_fields": updated_fields}}, HTTPStatus.INTERNAL_SERVER_ERROR

    def delete_event_by_id(self, event_id: str) -> Tuple[dict, HTTPStatus]:
        try:
            _, status_code = self.get_event_by_id(event_id)
            if status_code != HTTPStatus.OK:
                raise ValueError(f"Event with id {event_id} does not exist")

            self.events_repo.delete_event(event_id)
            return {"message": f"Event Deleted: event id={event_id} has been removed"}, HTTPStatus.OK
        except ValueError as value_err:
            return {"message": str(value_err)}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {"message": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR

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
