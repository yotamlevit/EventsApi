from DL.SqlExecutor import SqlExecutor


class BaseDLTest:
    def setup_class(self, table_name, table_columns , table_values, create_table_query):
        self.table_name = table_name
        self.table_columns = table_columns
        self.table_values = table_values
        self.sql_executor = SqlExecutor(db_name=':memory:')
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
