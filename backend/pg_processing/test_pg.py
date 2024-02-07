pytest_plugins = ['django']
import pytest
from .psycopg_module import BaseConnectionDB
from .kis_data import KISData, QuerySets


# Fixture to create a connection for testing
@pytest.fixture
def test_conn():
    connection = BaseConnectionDB(dbname='postgres', host='localhost', user='postgres', password='root')
    yield connection
    if connection.conn:
        connection.close_connection()


@pytest.fixture
def kis_data_instance():
    obj = KISData(QuerySets().queryset_for_dmk())
    return obj


# Testing psycopg_module, BaseConnectionDB class
def test_success_connection(test_conn):
    assert test_conn.conn is not None


def test_executing_get_queries(test_conn):
    result = test_conn.execute_query('SELECT schema_name FROM information_schema.schemata;')
    assert result[0][0] != 'Error'


# Testing kis_data module
def test_generator_closing(kis_data_instance):
    for i in kis_data_instance.get_data_generator():
        pass
    assert kis_data_instance.db_conn.connection_status == 1
