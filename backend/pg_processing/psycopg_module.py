#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Describes connection and sql queries to Postgres DB."""

from django.utils.translation import gettext as _
from psycopg2 import OperationalError, ProgrammingError
from psycopg2.errors import UndefinedTable, SyntaxError
import psycopg2
from collections import Counter
from .sql_queries import BASE_QUERY


class BaseConnectionDB:
    """
    Describes connection and SQL queries to a Postgres DB.

    This module provides classes for connecting to a PostgreSQL database, executing SQL queries,
    and handling various database-related operations.

    Classes:
    - BaseConnectionDB: Handles the base database connection and common operations.
    - ChangingQueriesDB: Extends BaseConnectionDB and provides functionality for executing custom SQL queries.

    Usage:
    1. Create an instance of BaseConnectionDB by providing connection parameters.
    2. Use methods like execute_query, _get_columns_list, and get_connection_data for database operations.

    Args:
    - user (str): The username for the database connection. Defaults to 'postgres'.
    - password (str): The password for the database connection. Defaults to 'root'.
    - dbname (str): The name of the database. Defaults to 'postgres'.
    - host (str): The host address of the database. Defaults to 'localhost'.
    - port (int): The port number for the database connection. Defaults to 5432.

    Attributes:
    - conn: The database connection instance if the connection is established successfully.
           Otherwise, a string with an error message.
    - cursor: The database cursor for executing SQL queries.
    """

    conn = None

    def __init__(self, **kwargs):
        """
        Pass the connection values to the database you need.

        - *user* (str): The username for the database connection. Defaults to 'postgres'.
        - *password* (str): The password for the database connection. Defaults to 'root'.
        - *dbname* (str): The name of the database. Defaults to 'postgres'.
        - *host* (str): The host address of the database. Defaults to 'localhost'.
        - *port* (int): The port number for the database connection. Defaults to 5432.

        :param kwargs: connection parameters of the database.
        """
        self.user = kwargs.get('user', 'postgres')
        self.password = kwargs.get('password', 'root')
        self.dbname = kwargs.get('dbname', 'postgres')
        self.host = kwargs.get('host', 'localhost')
        self.port = kwargs.get('port', 5432)
        self.__connect()

    # Private method that trying to establish connection and set result in class attribute.
    def __connect(self):
        """
        Private method to establish a database connection.

        Raises:
        - OperationalError: If the connection cannot be established.
        - UnicodeDecodeError: If there is an issue with decoding connection parameters.

        Returns:
        - None: If the connection is successful, otherwise sets an error message in self.conn.
        """
        try:
            self.conn = psycopg2.connect(user=self.user, password=self.password,
                                         dbname=self.dbname, host=self.host, port=self.port)
            self.cursor = self.conn.cursor()
        except (OperationalError, UnicodeDecodeError) as connection_error:
            self.conn = f'Проверьте данные подключения к БД (порт). Оригинальный текст ошибки: \n{connection_error}'
            if type(connection_error) is UnicodeDecodeError:
                self.conn = f'Проверьте данные подключения к БД. Неверные логин/пароль/хост.'
        return self.conn

    def _get_columns_list(self, table_name=None):
        """
        Get a list of column names for a given table.

        Args:
        - table_name (str): The name of the table.

        Returns:
        - list: A list of column names.
        """
        if type(self.conn) is str:
            return 'Class method get_column_names() can\'t be used with string object.'
        result = self.check_query(self.cursor, BaseSQLQueries.column_names_query)
        self._close_connection
        result = [column[0] for column in result]
        return result

    def _close_connection(self):
        """
        Closes the database connection and cursor.
        """
        if type(self.conn) is str:
            return
        self.cursor.close()
        self.conn.close()

    def check_query(self, cursor, query):
        """
        Helper method to execute a SQL query and handle errors.

        :param cursor: Database cursor.
        :param query: (str) A pure SQL query.
        :return: (list) Result set as a list of tuples or the exception object.
        """
        try:
            cursor.execute(query)
        except (UndefinedTable, SyntaxError, ProgrammingError) as err:
            return err
        return cursor.fetchall()

    def execute_query(self):
        """
        Execute a SQL query and return the result set.

        :param table_name: (str) A part of a fixed pure SQL query - table only.
        :return: Result set as a list of tuples.
        In case of an undefined table (UndefinedTable exception),
        the exception object is returned as an error.
        """
        if type(self.conn) is str:
            return self.conn
        result = self.check_query(self.cursor, BaseSQLQueries.base_query)
        self._close_connection
        counted_dict = Counter([item[0] for item in result])
        result = dict(counted_dict.items())
        return result

    def count_data(self, data):

        pass

    def get_connection_data(self):
        """
        Get the connection parameters of the database.

        :return: (dict) Dictionary containing database connection parameters.
        """
        return {
            'dbname': self.dbname,
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password
        }



