import sqlite3
from DL.SqlExecutor import SqlExecutor

import pytest
import sqlite3
from DL.SqlExecutor import SqlExecutor


@pytest.fixture(scope='session')
def table_metadata():
    return {
        "table_name": "test_table",
        "columns": ["id", "name"],
        "test_values": {
            'select_test': [1, "select_test"],
            'update_test': [2, "update_test"],
            'delete_test': [3, "delete_test"]

        } ,
        "create_table_query": '''
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        '''
    }


def insert_test_values(table_metadata, sql_executor):
    for _, test_values in table_metadata["test_values"].items():
        query = f'''INSERT INTO {table_metadata['table_name']} ({', '.join(table_metadata['columns'])}) VALUES ({', '.join(['?'] * len(table_metadata['columns']))})'''
        sql_executor.cursor.execute(query, test_values)


def unpack_test_values(table_metadata, test_name):
    return table_metadata['table_name'], *table_metadata['test_values'][test_name]

@pytest.fixture(scope='module')
def sql_executor(table_metadata):
    # Create the test table
    sql_executor = SqlExecutor(db_name=':memory:')

    sql_executor.cursor.execute(table_metadata['create_table_query'])

    # Add table data
    insert_test_values(table_metadata, sql_executor)

    return sql_executor


def test_select(sql_executor, table_metadata):
    table_name, id, name = unpack_test_values(table_metadata, 'select_test')
    condition = f'id = {id}'


    # Perform a select operation using SqlExecutor
    result_name = sql_executor.select(table_name, columns='name', condition=condition)
    result = sql_executor.select(table_name, condition=condition)

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
    columns = ['id', 'name']
    values = [9999, 'insert_test']

    # Perform the insert operation using SqlExecutor
    sql_executor.insert(table_metadata['table_name'], table_metadata['columns'], values)

    # Check if the data was inserted correctly
    sql_executor.cursor.execute(f'SELECT * FROM {table_metadata['table_name']} WHERE id=9999')
    result = sql_executor.cursor.fetchall()

    assert result == [(9999, 'insert_test')]


def test_delete(sql_executor, table_metadata):
    table_name, id, name = unpack_test_values(table_metadata, 'delete_test')
    condition = f'id = {id}'

    # Perform an update operation using SqlExecutor
    sql_executor.delete(table_name, condition=condition)

    # Check if the data was updated correctly
    sql_executor.cursor.execute(f'SELECT name FROM {table_name} WHERE {condition}')
    result = sql_executor.cursor.fetchall()

    assert result == []
