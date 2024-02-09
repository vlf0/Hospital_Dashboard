import pytest
from .psycopg_module import BaseConnectionDB
from .kis_data import QuerySets, DataForDMK, KISDataProcessing


# Fixture to create a connection for testing
@pytest.fixture
def test_conn():
    connection = BaseConnectionDB(dbname='postgres', host='localhost', user='postgres', password='root')

    class KISData:

        def __init__(self):
            self.db_conn = connection
            self.cursor = self.db_conn.execute_query

        def get_data_generator(self, query_sets):
            for dataset in query_sets:
                yield self.cursor(dataset[0])
            self.db_conn.close_connection()

    inst = KISData()
    yield inst
    if inst.db_conn.conn:
        inst.db_conn.close_connection()


# Testing BaseConnectionDB class
def test_success_connection(test_conn):
    """Checking attribute of class instance that is connection object."""
    assert test_conn.db_conn.conn is not None


def test_executing_get_queries(test_conn):
    """Checking successfully executing queries if connection is ok."""
    result = test_conn.db_conn.execute_query('SELECT schema_name FROM information_schema.schemata;')
    assert result[0][0] != 'Error'


# Testing kis_data module
def test_collecting_data(test_conn):
    """
    Checking that processing data for DMK methods always returns a dicts.
    It guarantees that serializer will work correct and returns serialized data.
    If connection error occur - then returned dicts will contain all zeros.
    """
    iterator = test_conn.get_data_generator(QuerySets().queryset_for_dmk())
    assert type(DataForDMK(iterator).get_arrived_data()) is dict
    assert type(DataForDMK(iterator).get_signout_data()) is dict
    assert type(DataForDMK(iterator).get_reanimation_data()) is dict


def test_creating_sr_kis_data(test_conn):
    """
    Checks that the method will work in any case, even if some PG error occurs within the program.
    If any errors occur, all serialized data will have null values
    (this allows data with null values  be treated as null on the front end).
    """
    class_instance = KISDataProcessing(test_conn.get_data_generator(QuerySets().queryset_for_kis()))
    assert type(class_instance.create_ready_dicts()) is list


def test_getting_columns(test_conn):
    columns = test_conn.db_conn.execute_query(QuerySets().COLUMNS['deads_t'])
    assert type(columns) is list and len(columns) != 0
