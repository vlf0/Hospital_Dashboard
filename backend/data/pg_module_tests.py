import pytest
from django.db import connections
from .psycopg_module import BaseConnectionDB

conn = connections.settings['kis_db']
DB_PARAMS = {
    'user': conn['USER'],
    'password': conn['PASSWORD'],
    'dbname': conn['NAME'],
    'host': conn['HOST'],
    'port': 5432
}


@pytest.fixture
def db_connection():
    db = BaseConnectionDB(**DB_PARAMS)
    yield db
    db.close_connection()


def test_connection_established(db_connection):
    """
    Test that the connection is established successfully.
    """
    assert db_connection.conn is not None


def test_invalid_connection():
    """
    Test that an invalid connection raises an error.
    """
    invalid_params = DB_PARAMS.copy()
    invalid_params['password'] = 'wrong_password'
    db = BaseConnectionDB(**invalid_params)
    assert db.conn is None


def test_execute_query(db_connection):
    """
    Test that a query executes successfully and returns expected results.
    """
    create_table_query = "CREATE TABLE IF NOT EXISTS mm.test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));"
    db_connection.execute_query(create_table_query)

    truncate_db_query = """TRUNCATE mm.test_table RESTART IDENTITY CASCADE;"""
    db_connection.execute_query(truncate_db_query)
    insert_query = """INSERT INTO mm.test_table (name) VALUES ('test_name') RETURNING id;"""
    result = db_connection.execute_query(insert_query)
    assert len(result) == 1

    select_query = """SELECT * FROM mm.test_table;"""
    result = db_connection.execute_query(select_query)
    assert len(result) == 1
    assert result[0][1] == 'test_name'


def test_query_error_handling(db_connection):
    """
    Test that an invalid query is handled correctly.
    """
    invalid_query = "SELECT * FROM mm.non_existing_table;"
    result = db_connection.execute_query(invalid_query)
    assert result is not list


def test_connection_status(db_connection):
    """
    Test the connection status property.
    """
    assert db_connection.connection_status == 0


def test_auto_close():
    """
    Test that the connection closes automatically when auto_close is True.
    """
    db = BaseConnectionDB(auto_close=True, **DB_PARAMS)
    create_table_query = "CREATE TABLE IF NOT EXISTS mm.test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));"
    db.execute_query(create_table_query)
    assert db.connection_status == 1
