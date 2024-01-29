import pytest
from .psycopg_module import BaseConnectionDB


# Fixture to create a connection for testing
@pytest.fixture
def test_conn():
    connection = BaseConnectionDB(dbname='postgres', host='localhost', user='postgres', password='root')
    yield connection
    if connection.conn:
        connection.close_connection()


def test_connection_creating(test_conn):
    assert test_conn.conn is not None


