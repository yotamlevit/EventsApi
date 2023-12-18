import sqlite3
from datetime import datetime
from typing import List


class SqlExecutor:
    _instance = None

    def __new__(cls, db_name='Application.db'):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.connection = sqlite3.connect(db_name, check_same_thread=False)
            cls._instance.cursor = cls._instance.connection.cursor()
        return cls._instance

    def select(self, table: str, columns='*', condition='', order_by=''):
        query = f"SELECT {columns} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        if order_by:
            query += f" ORDER BY {order_by}"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as sql_err:
            print(f"Error executing SELECT query: {sql_err}")
            raise sql_err

    def insert(self, table: str, columns: List[str], values: List[str]):
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(values))})"
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except sqlite3.Error as sql_err:
            print(f"Error executing INSERT query: {sql_err}")
            raise sql_err

    def update(self, table: str, update_values: dict, condition=''):
        set_keys = ', '.join([f'{key}=?' for key in update_values.keys()])
        set_values = list(update_values.values())

        query = f"UPDATE {table} SET {set_keys}"
        if condition:
            query += f" WHERE {condition}"
        try:
            self.cursor.execute(query, set_values)
            self.connection.commit()
        except sqlite3.Error as sql_err:
            print(f"Error executing UPDATE query: {sql_err}")
            raise sql_err

    def delete(self, table: str, condition=''):
        query = f"DELETE FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as sql_err:
            print(f"Error executing DELETE query: {sql_err}")
            raise sql_err

    def close_connection(self):
        try:
            self.connection.close()
        except sqlite3.Error as sql_err:
            print(f"Error closing connection: {sql_err}")
            raise sql_err
