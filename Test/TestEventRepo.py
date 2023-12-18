from datetime import datetime
from DTO import EventDTO
from DL import EventRepo
from .BaseTest import BaseEventsTest


class TestEventRepo(BaseEventsTest):

    def setup_class(self):
        test_table = "TestEventRepo"
        super().setup_class(self, test_table)

        self.event_repo = EventRepo(test_table)

    def test_get_event_by_id(self):
        id = 1
        result = self.event_repo.get_event_by_id(id)
        result_no_exists = self.event_repo.get_event_by_id(9999)

        expected_result = self.table_values[0]
        expected_result.insert(0, id)
        assert len(result) == 1
        assert result == [tuple(expected_result)]
        assert result_no_exists == []

    def test_get_event_by_location(self):
        result = self.event_repo.get_event_by_location('location')
        assert len(result) == len(self.table_values)

    def test_get_event_by_sort_key(self):
        result = self.event_repo.get_event_by_sort_key('id')
        assert result[0][0] == 1
        assert result[1][0] == 2

    def test_create_event(self):
        event_location = 'test_location'
        event = EventDTO(name='test_event', start_time=datetime.now(), team1='Team A', team2='Team B',
                         location=event_location, participants=100)
        self.event_repo.create_event(event)
        events = self.event_repo.get_event_by_location(event_location)
        assert len(events) == 1

    def test_update_event(self):
        updated_name = 'test_update_event'
        expected_result = self.table_values[1]
        expected_result[0] = updated_name

        id = 2
        expected_result.insert(0, id)
        update_values = {"name": updated_name}

        self.event_repo.update_event(id, update_values)

        updated_event = self.event_repo.get_event_by_id(id)
        assert len(updated_event) == 1
        assert updated_event == [tuple(expected_result)]

    def test_delete_event(self):
        self.event_repo.delete_event(1)
        result = self.event_repo.get_event_by_id(1)
        assert len(result) == 0

    def test_get_events(self):
        events = self.event_repo.get_events()
        self.event_repo.delete_all()
        no_events_result = self.event_repo.get_events()
        assert isinstance(events, list)
        assert no_events_result == []

