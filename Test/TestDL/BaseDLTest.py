from DL.SqlExecutor import SqlExecutor

class BaseDLTest:
    @classmethod
    def setup_class(cls, table_name, table_columns , table_values, create_table_query):
        cls.table_name = table_name
        cls.table_columns = table_columns
        cls.table_values = table_values
        cls.sql_executor = cls.__init_sql_executor(cls, create_table_query)
        cls.__insert_test_values(cls)

    def __init_sql_executor(self, create_table_query):
        # Create the test table
        sql_executor = SqlExecutor(db_name=':memory:')
        sql_executor.cursor.execute(create_table_query)

        return sql_executor

    def __insert_test_values(self):
        for test_value in self.table_values:
            query = f'''INSERT INTO {self.table_name} ({', '.join(self.table_columns)}) VALUES ({', '.join(['?'] * len(self.table_columns))})'''
            self.sql_executor.cursor.execute(query, test_value)
