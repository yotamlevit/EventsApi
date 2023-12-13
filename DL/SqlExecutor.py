import sqlite3
from datetime import datetime

class SqlExecutor:
    _instance = None

    def __new__(cls, db_name='Application.db'):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.connection = sqlite3.connect(db_name, check_same_thread=False)
            cls._instance.cursor = cls._instance.connection.cursor()
        return cls._instance

    def select(self, table, columns='*', condition='', params=None):
        query = f"SELECT {columns} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Error executing SELECT query: {e}")

    def insert(self, table, columns, values):
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(values))})"
        print(query)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error executing INSERT query: {e}")

    def update(self, table, values, condition='', params=None):
        set_values = ', '.join([f"{col} = ?" for col in values])
        query = f"UPDATE {table} SET {set_values}"
        if condition:
            query += f" WHERE {condition}"
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error executing UPDATE query: {e}")

    def delete(self, table, condition='', params=None):
        query = f"DELETE FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error executing DELETE query: {e}")

    def close_connection(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing connection: {e}")
