from .BaseTest import BaseTest


class TestSqlExecutor(BaseTest):

    def setup_class(self):
        table_name = 'test_table'
        table_columns = {"name": "TEXT", "value1": "TEXT"}
        table_values = [["select_test", "value1"], ["update_test", "value2"], ["delete_test", "value3"]]
        super().setup_class(self, table_name=table_name, table_columns=table_columns, table_values=table_values)

    def test_select(self):
        test_name = 'select_test'
        condition = f'name="{test_name}"'


        # Perform a select operation using SqlExecutor
        result_name = self.sql_executor.select(self.table_name, columns='name', condition=condition)

        result = self.sql_executor.select(self.table_name)

        assert result_name == [(test_name,)]


    def test_update(self):
        name = 'update_test'
        condition = f'name = "{name}"'
        updated_name = 'UpdatedName'

        # Perform an update operation using SqlExecutor
        update_values = {'name': updated_name}
        self.sql_executor.update(self.table_name, update_values, condition=condition)
        condition = f'name = "{updated_name}"'

        # Check if the data was updated correctly
        self.sql_executor.cursor.execute(f'SELECT name FROM {self.table_name} WHERE {condition}')
        result = self.sql_executor.cursor.fetchall()

        print(result)
        assert result == [(updated_name,)]


    def test_insert(self):
        values = ['insert_test', "value"]

        # Perform the insert operation using SqlExecutor
        self.sql_executor.insert(self.table_name, self.table_columns, values)

        # Check if the data was inserted correctly
        self.sql_executor.cursor.execute(f'SELECT * FROM {self.table_name} WHERE name="insert_test"')
        result = self.sql_executor.cursor.fetchall()

        assert result[0][1:] == tuple(values)


    def test_delete(self):
        name = 'delete_test'
        condition = f'name = "{name}"'

        # Perform an update operation using SqlExecutor
        self.sql_executor.delete(self.table_name, condition=condition)

        # Check if the data was updated correctly
        self.sql_executor.cursor.execute(f'SELECT name FROM {self.table_name} WHERE {condition}')
        result = self.sql_executor.cursor.fetchall()

        assert result == []
