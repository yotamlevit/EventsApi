import sqlite3
from datetime import datetime
from DL.SqlExecutor import SqlExecutor
from BL.DTO import EventDTO
import pytz


class UsersRepo:
    def __init__(self, table='users'):
        self.sql_executor = SqlExecutor()
        self.table = table
        self.fields = list(EventDTO.model_fields.keys())
        self.fields.append("creation_time")

    def get_events(self):
        try:
            return self.sql_executor.select(self.table)
        except sqlite3.Error as sql_err:
            raise Exception(f"Unexpected error retrieving events: {sql_err}")

    def get_event_by_id(self, event_id: int):
        try:
            return self.sql_executor.select(self.table, condition=f'id={event_id}')
        except sqlite3.Error as sql_err:
            raise Exception(f"Unexpected error retrieving events: {sql_err}")

    def get_event_by_location(self, event_location: str):
        try:
            return self.sql_executor.select(self.table, condition=f'location="{event_location}"')
        except sqlite3.Error as sql_err:
            raise Exception(f"Unexpected error retrieving events : {sql_err}")

    def get_event_by_sort_key(self, sort_key: str):
        try:
            return self.sql_executor.select(self.table, order_by=sort_key)
        except sqlite3.Error as sql_error:
            if sql_error.sqlite_errorcode == 1:
                raise ValueError(f'Invalid sort key key={sort_key}')
            raise Exception(f"Unexpected error retrieving events: {sql_error} with sort key={sort_key}")

    def get_upcoming_events(self):
        try:
            current_time = pytz.utc.localize(datetime.now())
            time_condition = f'start_time > "{current_time}"'
            upcoming_events = self.sql_executor.select(self.table, condition=time_condition)
            return upcoming_events
        except sqlite3.Error as sql_err:
            raise Exception(f"Unexpected error while fetching upcoming events: {sql_err}")

    def create_event(self, event: EventDTO):
        try:
            insertion_time = pytz.utc.localize(datetime.now())
            event_values = list(event.__dict__.values())
            event_values.append(insertion_time)
            self.sql_executor.insert(self.table, self.fields, event_values)
        except sqlite3.Error as sql_err:
            raise Exception(f"Unexpected error while inserting new events: {sql_err}")

    def update_event(self, event_id: int, updated_fields: dict, ):
        try:
            if not set(list(updated_fields.keys())).issubset(self.fields[:-1]):
                raise ValueError

            self.sql_executor.update(self.table, updated_fields, condition=f'id={event_id}')

        except sqlite3.Error as sql_err:
            raise Exception(f"Unexpected error while updating event: {sql_err}")
        except ValueError:
            raise ValueError(f'Invalid field to update. The allowd fields are: {self.fields[:-1]}')

    def delete_event(self, event_id: int):
        try:
            self.sql_executor.delete(self.table, condition=f'id={event_id}')
        except sqlite3.Error as sql_err:
            raise Exception(f"Unexpected error while deleting event: {sql_err}")

    def delete_all(self):
        try:
            self.sql_executor.delete(self.table)
        except sqlite3.Error as sql_err:
            raise Exception(f"Unexpected error while deleting event: {sql_err}")
