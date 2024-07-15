import pytest
from .psycopg_module import BaseConnectionDB


@pytest.mark.usefixtures('connect_to_kisdb')
class TestBaseConnecection:

    def test_connection_established(self):
        """
        Test that the connection is established successfully.
        """
        assert self.conn is not None

    def test_invalid_connection(self):
        """
        Test that an invalid connection raises an error.
        """
        invalid_params = {'host': 'localhost',
                          'dbname': 'kis',
                          'user': 'wrong_login',
                          'password': 'wrong_password'}
        db = BaseConnectionDB(**invalid_params)
        assert db.conn is None

    def test_connection(self):
        assert self.conn.connection_status == 0

    def test_execute_query(self):
        """
        Test that a query executes successfully and returns expected results.
        """
        transaction = """
            CREATE SCHEMA IF NOT EXISTS mm;
            CREATE TABLE IF NOT EXISTS mm.test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));
            INSERT INTO mm.test_table (name) VALUES ('test_name') RETURNING id;
            """
        self.conn.execute_query(transaction, insert=True)
        select_query = """SELECT * FROM mm.test_table;"""
        result = self.conn.execute_query(select_query)
        assert result[0][1] == 'test_name'

    def test_query_error_handling(self):
        """
        Test that an invalid query is handled correctly.
        """
        invalid_query = "SELECT * FROM mm.non_existing_table;"
        result = self.conn.execute_query(invalid_query)
        assert result is not list

    def test_auto_close(self):
        """
        Test that the connection closes automatically when auto_close is True.
        """
        creds = self.conn.get_connection_data
        db = BaseConnectionDB(auto_close=True, **creds)
        create_table_query = "CREATE TABLE IF NOT EXISTS mm.test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));"
        db.execute_query(create_table_query)
        assert db.connection_status == 1
