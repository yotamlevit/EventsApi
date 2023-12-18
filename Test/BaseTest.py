from DL.SqlExecutor import SqlExecutor


class BaseTest:
    def setup_class(self, table_name, table_columns , table_values):
        self.table_name = table_name
        self.table_columns = list(table_columns.keys())
        self.table_values = table_values
        self.sql_executor = SqlExecutor(db_name=':memory:')

        parsed_columns = [f"{key} {type}" for key, type in table_columns.items()]
        parsed_columns.insert(0, 'id INTEGER')
        parsed_columns.append('PRIMARY KEY("id" AUTOINCREMENT)')
        create_table_query = f'''CREATE TABLE {table_name} ({', '.join(parsed_columns)})'''

        self.__create_test_table(self, create_table_query=create_table_query)

    def __insert_test_values(self):
        for test_value in self.table_values:
            query = f'''INSERT INTO {self.table_name} ({', '.join(self.table_columns)}) VALUES ({', '.join(['?'] * len(self.table_columns))})'''
            self.sql_executor.cursor.execute(query, test_value)

    def __check_table_exist(self):
        self.sql_executor.cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
        tables = self.sql_executor.cursor.fetchall()
        tables = [table[0] for table in tables]
        return self.table_name in tables

    def __create_test_table(self, create_table_query):
        if not self.__check_table_exist(self):
            self.sql_executor.cursor.execute(create_table_query)
            self.__insert_test_values(self)


class BaseEventsTest(BaseTest):
    def setup_class(self, table_name):
        table_columns = {"name": "Text",
                         "start_time": "TEXT",
                         "team1": "TEXT",
                         "team2": "TEXT",
                         "location": "TEXT",
                         "participants": "INTEGER",
                         "creation_time": "TEXT"}

        table_values = [["event1", "time", "team1", "team2", "location", "participants", "creation_time"],
                        ["event2", "time", "team1", "team2", "location", "participants", "creation_time"],
                        ["event3", "time", "team1", "team2", "location", "participants", "creation_time"],]

        super().setup_class(self, table_name=table_name, table_columns=table_columns, table_values=table_values)
