from Test.TestDL.Arrange import table_metadata, unpack_test_values, sql_executor


def test_select(sql_executor, table_metadata):
    table_name, id, name = unpack_test_values(table_metadata, 'select_test')
    condition = f'id = {id}'


    # Perform a select operation using SqlExecutor
    result_name = sql_executor.select(table_name, columns='name', condition=condition)
    result = sql_executor.select(table_name, columns='id, name', condition=condition)

    assert result_name == [(name,)]
    assert result == [(id, name)]


def test_update(sql_executor, table_metadata):
    table_name, id, name = unpack_test_values(table_metadata, 'update_test')
    condition = f'id = {id}'
    updated_name = 'UpdatedName'

    # Perform an update operation using SqlExecutor
    update_values = {'name': updated_name}
    sql_executor.update(table_name, update_values, condition=condition)

    # Check if the data was updated correctly
    sql_executor.cursor.execute(f'SELECT name FROM {table_name} WHERE {condition}')
    result = sql_executor.cursor.fetchall()

    assert result == [(updated_name,)]


def test_insert(sql_executor, table_metadata):
    values = [9999, 'insert_test', "date", "team1", "team2", "location", 0, "insertion_time"]

    # Perform the insert operation using SqlExecutor
    sql_executor.insert(table_metadata['table_name'], table_metadata['columns'], values)

    # Check if the data was inserted correctly
    sql_executor.cursor.execute(f'SELECT * FROM {table_metadata['table_name']} WHERE id=9999')
    result = sql_executor.cursor.fetchall()

    assert result == [tuple(values)]


def test_delete(sql_executor, table_metadata):
    table_name, id, name = unpack_test_values(table_metadata, 'delete_test')
    condition = f'id = {id}'

    # Perform an update operation using SqlExecutor
    sql_executor.delete(table_name, condition=condition)

    # Check if the data was updated correctly
    sql_executor.cursor.execute(f'SELECT name FROM {table_name} WHERE {condition}')
    result = sql_executor.cursor.fetchall()

    assert result == []
