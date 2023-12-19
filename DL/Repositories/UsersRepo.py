import sqlite3
from DL.SqlExecutor import SqlExecutor
from BL.DTO import EventDTO


class UsersRepo:
    def __init__(self, table='users'):
        self.sql_executor = SqlExecutor()
        self.table = table
        self.fields = list(EventDTO.model_fields.keys())

    def get_users(self):
        try:
            return self.sql_executor.select(self.table)
        except sqlite3.Error as sql_err:
            raise Exception(f"Unexpected error retrieving Users: {sql_err}")

    def get_user_by_username(self, username: int):
        try:
            return self.sql_executor.select(self.table, condition=f'username={username}')
        except sqlite3.Error as sql_err:
            raise Exception(f"Unexpected error retrieving Users: {sql_err}")