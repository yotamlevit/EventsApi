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
        self.fields.append("insertion_time")

    def add_event(self, event: EventDTO, insertion_time: datetime):
        try:
            event_values = list(event.__dict__.values())
            event_values.append(insertion_time)
            print(event_values)
            self.sql_executor.insert(self.table, self.fields, event_values)
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