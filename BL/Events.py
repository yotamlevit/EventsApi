from BL.Logger import Logger as logging
from datetime import datetime
from typing import Tuple
import pytz
from http import HTTPStatus
from DTO import EventDTO
from DL import EventRepo
from .Utils import parse_event

class EventManager:
    def __init__(self, user_permissions):
        self.events_repo = EventRepo()
        self.user_permissions = 1

    def get_events(self) -> Tuple[list, HTTPStatus]:
        try:
            events = self.events_repo.get_events()
            if events:
                events = [parse_event(event) for event in events]

                logging.info("Successfully fetched all events", response=events, http_code=HTTPStatus.OK)
                return events, HTTPStatus.OK
            else:
                response = {"message": "There are no events at the moment"}
                logging.info("Events table empty", response=response, http_code=HTTPStatus.NOT_FOUND)
                return response, HTTPStatus.NOT_FOUND

        except Exception as err:
            response = {"message": str(err)}
            logging.error(response['message'], response=response, http_code=HTTPStatus.INTERNAL_SERVER_ERROR, error=err)
            return {"message": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_event_by_id(self, event_id: str) -> Tuple[dict, HTTPStatus]:
        try:
            event = self.events_repo.get_event_by_id(event_id)
            if event:
                response = parse_event(event[0])
                logging.info(f"Successfully fetched event id={event_id}", response=response, http_code=HTTPStatus.OK)
                return response, HTTPStatus.OK
            else:
                response = {"message": f"Event id={event_id} not found"}
                logging.info(response['message'], response=response, http_code=HTTPStatus.NOT_FOUND)
                return response, HTTPStatus.NOT_FOUND
        except Exception as err:
            response = {"message": str(err)}
            logging.error(f"{response['message']} where id={event_id}", response=response, http_code=HTTPStatus.INTERNAL_SERVER_ERROR, error=err)
            return response, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_event_by_location(self, event_location: str) -> Tuple[dict, HTTPStatus]:
        try:
            events = self.events_repo.get_event_by_location(event_location)
            if events:
                events = [parse_event(event) for event in events]
                logging.info("Successfully fetched events", response=events, http_code=HTTPStatus.OK)
                return events, HTTPStatus.OK
            else:
                response = {"message": f"Events location={event_location} not found"}
                logging.info(response['message'], response=response, http_code=HTTPStatus.NOT_FOUND)
                return response, HTTPStatus.NOT_FOUND
        except Exception as err:
            response = {"message": str(err)}
            logging.error(f"{response['message']} where location={event_location}", response=response, http_code=HTTPStatus.INTERNAL_SERVER_ERROR, error=err)
            return response, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_event_by_sort_key(self, sort_key: str) -> Tuple[list, HTTPStatus]:
        try:
            events = self.events_repo.get_event_by_sort_key(sort_key)
            if events:
                events = [parse_event(event) for event in events]
                logging.info(f"Successfully fetched events orders by {sort_key}", response=events, http_code=HTTPStatus.OK)
                return events, HTTPStatus.OK
            else:
                response = {"message": "There are no events at the moment"}
                logging.info("Events table empty", response=response, http_code=HTTPStatus.NOT_FOUND)
                return response, HTTPStatus.NOT_FOUND
        except ValueError as value_err:
            response = {"message": str(value_err)}
            logging.error(response['message'], response=response, http_code=HTTPStatus.BAD_REQUEST, error=value_err)
            return response, HTTPStatus.BAD_REQUEST
        except Exception as err:
            response = {"message": str(err)}
            logging.error(response['message'], response=response, http_code=HTTPStatus.INTERNAL_SERVER_ERROR, error=err)
            return response, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_upcoming_events(self):
        try:
            upcoming_events = self.events_repo.get_upcoming_events()
            if upcoming_events:
                response = [parse_event(event) for event in upcoming_events]

                logging.info("Successfully fetched upcoming events", response=response, http_code=HTTPStatus.OK)
                return upcoming_events, HTTPStatus.OK
            else:
                response = {"message": "There are no upcoming events (events in 30 minutes)"}
                logging.info(response['message'], response=response, http_code=HTTPStatus.NOT_FOUND)
                return response, HTTPStatus.NOT_FOUND
        except Exception as err:
            response = {"message": str(err)}
            logging.error(response['message'], response=response, http_code=HTTPStatus.INTERNAL_SERVER_ERROR, error=err)
            return response, HTTPStatus.INTERNAL_SERVER_ERROR

    def create_event(self, event: EventDTO) -> Tuple[dict, HTTPStatus]:
        try:
            if event.start_time > pytz.utc.localize(datetime.now()):
                self.events_repo.create_event(event)
                events, _ = self.get_event_by_sort_key("id")
                response = {"message": "Event created", "event_id": events[-1]["id"]}
                http_code = HTTPStatus.OK
            else:
                response = {"message": f"Error scheduling event: event time has already past"}
                http_code = HTTPStatus.BAD_REQUEST

            logging.info(response['message'], payload=event, response=response, http_code=http_code)
            return response, http_code
        except TypeError as type_err:
            response = {"message": str(type_err)}
            logging.info(response['message'], payload=event, response=response, http_code=HTTPStatus.BAD_REQUEST)
            return response, HTTPStatus.BAD_REQUEST
        except Exception as err:
            response = {"message": f"Error creating new event: {str(err)}", "event_data": event.__dict__}
            logging.error(response['message'], payload=event, response=response, http_code=HTTPStatus.INTERNAL_SERVER_ERROR, error=err)
            return response, HTTPStatus.INTERNAL_SERVER_ERROR

    def update_event(self, event_id: int, updated_fields: dict) -> Tuple[dict, HTTPStatus]:
        try:
            if not self.__event_exists(event_id):
                raise ValueError(f"Event with id {event_id} does not exist")

            self.events_repo.update_event(event_id, updated_fields)

            response = {"message": f"Event id={event_id} updated", "event_data": {"id": event_id, "update_fields": updated_fields}}
            logging.info(response['message'], payload=updated_fields, response=response, http_code=HTTPStatus.OK)
            return response, HTTPStatus.OK
        except ValueError as value_err:
            response = {"message": f"Cannot update event - {str(value_err)}", "event_data": {"id": event_id, "update_fields": updated_fields}}
            logging.info(response['message'], payload=updated_fields, response=response, http_code=HTTPStatus.BAD_REQUEST, error=value_err)
            return response, HTTPStatus.BAD_REQUEST
        except Exception as err:
            response = {"message": str(err), "event_data": {"id": event_id, "update_fields": updated_fields}}
            logging.info(response['message'], payload=updated_fields, response=response, http_code=HTTPStatus.INTERNAL_SERVER_ERROR, error=err)
            return response, HTTPStatus.INTERNAL_SERVER_ERROR

    def delete_event_by_id(self, event_id: str) -> Tuple[dict, HTTPStatus]:
        try:
            if not self.__event_exists(event_id):
                raise ValueError(f"Event with id {event_id} does not exist")

            self.events_repo.delete_event(event_id)
            return {"message": f"Event Deleted: event id={event_id} has been removed"}, HTTPStatus.OK
        except ValueError as value_err:
            response = {"message": f"Cannot delete event - {str(value_err)}"}
            logging.info(response['message'], response=response, http_code=HTTPStatus.BAD_REQUEST, error=value_err)
            return response, HTTPStatus.BAD_REQUEST
        except Exception as err:
            response = {"message": str(err)}
            logging.error(f"Error deleting event: {str(err)}", response=response, http_code=HTTPStatus.INTERNAL_SERVER_ERROR, error=err)
            return response, HTTPStatus.INTERNAL_SERVER_ERROR

    def __event_exists(self, event_id: str) -> bool:
        _, status_code = self.get_event_by_id(event_id)
        return status_code == HTTPStatus.OK
