
from datetime import datetime, timedelta
from DTO import EventDTO
from BL import EventActions
from .BaseTest import BaseEventsTest
import pytz
from http import HTTPStatus


class TestEvents(BaseEventsTest):
    def setup_class(self):
        super().setup_class(self, "events")
        self.event_manager = EventActions(1)

    def test_get_event_by_id(self):
        id = 1
        invalid_id = 9999
        response, status_code = self.event_manager.get_event_by_id(id)
        not_found_response, not_found_status_code = self.event_manager.get_event_by_id(invalid_id)

        expected_result = self.table_values[0]
        expected_result.insert(0, id)

        assert status_code == HTTPStatus.OK
        assert response['id'] == id

        assert not_found_status_code is HTTPStatus.NOT_FOUND
        assert not_found_response == {"message": f"Event id={invalid_id} not found"}

    def test_get_event_by_location(self):
        unreal_location = 'not_a_real_location'
        response, status_code = self.event_manager.get_event_by_location('location')
        not_found_response, not_found_status_code = self.event_manager.get_event_by_location(unreal_location)

        assert status_code is HTTPStatus.OK
        assert isinstance(response, list)

        assert not_found_status_code is HTTPStatus.NOT_FOUND
        assert not_found_response == {"message": f"Events location={unreal_location} not found"}

    def test_get_event_by_sort_key(self):
        invalid_key = 'not_a_valid_key'
        response, status_code = self.event_manager.get_event_by_sort_key('id')
        bad_key_response, bad_key_status_code = self.event_manager.get_event_by_sort_key(invalid_key)

        assert status_code is HTTPStatus.OK
        assert response[0]['id'] == 1
        assert response[1]['id'] == 2

        assert bad_key_status_code is HTTPStatus.BAD_REQUEST
        assert bad_key_response == {"message": f"Invalid sort key key={invalid_key}"}

    def test_create_event(self):
        event_location = 'test_create_location'
        event = EventDTO(name='test_event', start_time=pytz.utc.localize(datetime.now() + timedelta(days=10)), team1='Team A', team2='Team B',
                         location=event_location, participants=100)
        past_time_event = EventDTO(name='test_event', start_time=pytz.utc.localize(datetime.now()), team1='Team A', team2='Team B',
                         location=event_location, participants=100)
        bad_time_event = EventDTO(name='test_event', start_time=datetime.now(), team1='Team A', team2='Team B',
                                  location=event_location, participants=100)

        response, status_code = self.event_manager.create_event(event)
        event_id = response["event_id"]
        bad_time_response, bad_time_status_code = self.event_manager.create_event(bad_time_event)
        past_time_response, past_time_status_code = self.event_manager.create_event(past_time_event)


        _, check_status_code = self.event_manager.get_event_by_id(event_id)

        assert status_code is HTTPStatus.OK
        assert response["message"] == "Event created"
        assert check_status_code is HTTPStatus.OK

        assert bad_time_status_code is HTTPStatus.BAD_REQUEST
        assert bad_time_response == {"message": "can't compare offset-naive and offset-aware datetimes"}

        assert past_time_status_code is HTTPStatus.BAD_REQUEST
        assert past_time_response == {"message": "Error scheduling event: event time has already past"}

    def test_update_event(self):
        updated_name = 'test_update_event'
        id = 2
        invalid_id = 999
        update_values = {"name": updated_name}

        response, status_code = self.event_manager.update_event(id, update_values)
        id_not_exists_response, id_not_exists_status_code = self.event_manager.update_event(invalid_id, update_values)

        update_values = {"not_name": updated_name}
        invalid_field_response, invalid_field_status_code = self.event_manager.update_event(id, update_values)

        updated_event, _ = self.event_manager.get_event_by_id(id)

        assert status_code is HTTPStatus.OK
        assert response == {"message": f"Event id={id} updated","event_data": {"id": id,"update_fields": {"name": "test_update_event"}}}

        assert id_not_exists_status_code is HTTPStatus.BAD_REQUEST
        assert id_not_exists_response == {"message": f"Cannot update event - Event with id {invalid_id} does not exist","event_data": {"id": invalid_id,"update_fields": {"name": "test_update_event"}}}

        assert invalid_field_status_code is HTTPStatus.BAD_REQUEST
        assert invalid_field_response == {"message": "Cannot update event - Invalid field to update. The allowd fields are: ['name', 'start_time', 'team1', 'team2', 'location', 'participants']","event_data": {"id": id,"update_fields": {"not_name": "test_update_event"}}}

    def test_delete_event_by_id(self):
        id=1
        response, status_code = self.event_manager.delete_event_by_id(id)
        _, not_found_status_code = self.event_manager.get_event_by_id(id)
        bad_delete_response, bad_delete_status_code = self.event_manager.delete_event_by_id(id)
        assert status_code is HTTPStatus.OK
        assert response == {"message": f"Event Deleted: event id={id} has been removed"}
        assert not_found_status_code is HTTPStatus.NOT_FOUND
        assert bad_delete_status_code is HTTPStatus.BAD_REQUEST
        assert bad_delete_response == {"message": f"Cannot delete event - Event with id {id} does not exist"}

    def test_get_events(self):
        events, status_code = self.event_manager.get_events()
        self.event_manager.events_repo.delete_all()
        no_events_response, no_events_status_code = self.event_manager.get_events()
        assert status_code is HTTPStatus.OK
        assert isinstance(events, list)
        assert no_events_status_code is HTTPStatus.NOT_FOUND
        assert no_events_response == {"message": "There are no events at the moment"}
