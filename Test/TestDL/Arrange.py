import pytest

from DL.SqlExecutor import SqlExecutor


@pytest.fixture(scope='module')
def table_metadata():
    return {
        "table_name": "test_table",
        "columns": ["id", "name", "date", "team1", "team2", "location", "participants", "insertion_time"],
        "test_values": {
            'select_test': [1, "select_test", "date", "team1", "team2", "location", 0, "insertion_time"],
            'update_test': [2, "update_test", "date", "team1", "team2", "location", 0, "insertion_time"],
            'delete_test': [3, "delete_test", "date", "team1", "team2", "location", 0, "insertion_time"]

        } ,
        "create_table_query": '''
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                date TEXT,
                team1 TEXT,
                team2 TEXT,
                location TEXT,
                participants INTEGER,
                insertion_time TEXT
            )
        '''
    }



def unpack_test_values(table_metadata, test_name):
    return table_metadata['table_name'], *table_metadata['test_values'][test_name][0:2]



def insert_test_values(table_metadata, sql_executor):
    for _, test_values in table_metadata["test_values"].items():
        query = f'''INSERT INTO {table_metadata['table_name']} ({', '.join(table_metadata['columns'])}) VALUES ({', '.join(['?'] * len(table_metadata['columns']))})'''
        sql_executor.cursor.execute(query, test_values)

@pytest.fixture(scope='module')
def sql_executor(table_metadata):
    # Create the test table
    sql_executor = SqlExecutor(db_name=':memory:')

    sql_executor.cursor.execute(table_metadata['create_table_query'])

    # Add table data
    insert_test_values(table_metadata, sql_executor)

    return sql_executor
