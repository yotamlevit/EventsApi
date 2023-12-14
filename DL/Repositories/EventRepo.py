import sqlite3
from datetime import datetime
from DL.SqlExecutor import SqlExecutor
from BL import EventDTO
import inspect

class EventRepo:

    def __init__(self):
        self.sql_executor = SqlExecutor()
        self.table = 'events'
        self.fields = list(EventDTO.model_fields.keys())
        #self.fields.insert(0, 'id')
        self.fields.append("insertion_time")

    def get_events(self):
        try:
            return self.sql_executor.select(self.table)
        except sqlite3.Error as sql_err:
            print(f"Error retrieving event: {sql_err}")
            raise Exception(f"Unexpected error retrieving events")

    def get_event_by_id(self, event_id):
        try:
            return self.sql_executor.select(self.table, condition=f'id={event_id}')
        except sqlite3.Error as sql_err:
            print(f"Error retrieving event: {sql_err}")
            raise Exception(f"Unexpected error retrieving events")

    def get_event_by_location(self, event_location):
        try:
            return self.sql_executor.select(self.table, condition=f'location="{event_location}"')
        except sqlite3.Error as sql_err:
            print(f"Error retrieving event: {sql_err}")
            raise Exception(f"Unexpected error retrieving events")

    def get_event_by_sort_key(self, sort_key):
        try:
            return self.sql_executor.select(self.table, order_by=sort_key)
        except sqlite3.Error as sql_error:
            if sql_error.sqlite_errorcode == 1:
                raise ValueError(f'Invalid sort key key={sort_key}')
            print(f"Error retrieving event: {sql_error}")
            raise Exception(f"Unexpected error retrieving events")

    def create_event(self, event: EventDTO, insertion_time: datetime):
        try:
            event_values = list(event.__dict__.values())
            event_values.append(insertion_time)
            print(event_values)
            self.sql_executor.insert(self.table, self.fields, event_values)
        except sqlite3.Error as sql_err:
            print(f"Error adding event: {sql_err}")
            raise Exception(f"Unexpected error whhile inserting new events")

    def update_event(self, event_id: int, updated_fields: dict, ):
        try:
            self.sql_executor.update(self.table, updated_fields, condition=f'id={event_id}')
        except sqlite3.Error as sql_error:
            print(f"Error updating event: {sql_error}")

    def delete_event(self, event_id: str):
        try:
            self.sql_executor.delete(self.table, condition=f'id={event_id}')
        except sqlite3.Error as e:
            print(f"Error deleting event: {e}")

    def close_connection(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing connection: {e}")
