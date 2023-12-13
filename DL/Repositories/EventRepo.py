import sqlite3
from datetime import datetime
from DL.SqlExecutor import SqlExecutor

class EventDB:
    _instance = None

    def __init__(self):
        self.db = SqlExecutor()

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

    def close_connection(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing connection: {e}")
