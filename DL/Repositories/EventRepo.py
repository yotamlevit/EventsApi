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
        return self.sql_executor.select(self.table)

    def get_event_by_id(self, event_id):
        try:
            return self.sql_executor.select(self.table, condition=f'id={event_id}')
        except sqlite3.Error as e:
            print(f"Error retrieving event: {e}")

    def get_event_by_location(self, event_location):
        try:
            return self.sql_executor.select(self.table, condition=f'location="{event_location}"')
        except sqlite3.Error as e:
            print(f"Error retrieving event: {e}")

    def get_event_by_sort_key(self, sort_key):
        try:
            return self.sql_executor.select(self.table, order_by=sort_key)
        except sqlite3.Error as e:
            print(f"Error retrieving event: {e}")

    def create_event(self, event: EventDTO, insertion_time: datetime):
        try:
            event_values = list(event.__dict__.values())
            event_values.append(insertion_time)
            print(event_values)
            self.sql_executor.insert(self.table, self.fields, event_values)
        except sqlite3.Error as e:
            print(f"Error adding event: {e}")

    """
    def update_event(self, event_id: int, event: EventDTO):
        try:
            event_values = [getattr(event, field) for field in self.fields if field != 'id']
            event_values.append(datetime.now())  # Adding current time for modification
            condition = f'id={event_id}'  # Assuming 'id' is the primary key

            self.sql_executor.update(self.table, event_values, condition)
        except sqlite3.Error as e:
            print(f"Error updating event: {e}")
    """

    def update_event(self, event_id: int, updated_fields: dict, ):
        try:
            print(updated_fields)
            self.sql_executor.update(self.table, updated_fields, condition=f'id={event_id}')
        except sqlite3.Error as e:
            print(f"Error updating event: {e}")

    def delete_event(self, event_id: str):
        try:
            self.sql_executor.delete(self.table, condition=f'id={event_id}')
            #self.cursor.execute('DELETE FROM events WHERE id = ?', (event_id))
            #self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting event: {e}")

    def close_connection(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing connection: {e}")


"""
    def add_event(self, id: int, name: str, date: datetime, team1: str, team2: str, location: str, participants: int, creation_time: datetime):
        try:
            self.cursor.execute('''
                INSERT INTO events (id, name, date, team1, team2, location, creation_time, participants)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (id, name, date, team1, team2, location, creation_time, participants))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding event: {e}")

    def get_event_by_id(self, event_id):
        try:
            self.cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving event: {e}")

    def delete_event(self, event_id: str):
        try:
            self.cursor.execute('DELETE FROM events WHERE id = ?', (event_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting event: {e}")
            
"""