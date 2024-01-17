#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Describes connection and sql queries to Postgres DB."""

from psycopg2 import OperationalError, ProgrammingError
from psycopg2.errors import UndefinedTable, SyntaxError
import psycopg2


class BaseConnectionDB:
    """
    Describes connection and SQL queries to a Postgres DB.

    This module provides classes for connecting to a PostgreSQL database, executing SQL queries,
    and handling various database-related operations.

    Classes:
    - BaseConnectionDB: Handles the base database connection and common operations.

    Usage:
    1. Create an instance of BaseConnectionDB by providing connection parameters.
    2. Use methods like execute_query, and get_connection_data for database operations.

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
        return self.conn

    def _close_connection(self):
        """
        Close the database connection and cursor.

        :return: None
        """
        if type(self.conn) is str:
            return
        self.cursor.close()
        self.conn.close()

    def execute_query(self, query):
        """
        Execute a SQL query and return the result set based on the query type.

        :param query: (str or list): A SQL query string or a list containing the query and its parameters.
        :return: List of tuples. In case of an error (UndefinedTable, SyntaxError, ProgrammingError, TypeError),
        the exception object is returned.
        """
        if type(self.conn) is str:
            return self.conn

        try:
            if type(query) is str:
                result = self.get_query(query)
                return result
            self.insert_query(query)
        except (UndefinedTable, SyntaxError, ProgrammingError, TypeError) as err:
            return err

    def get_query(self, query):
        """
        Execute a get SQL query and return the result set.

        :param query: (str) A part of a fixed pure SQL query - table only.
        :return: Result set as a list of tuples.
        In case of an undefined table (UndefinedTable exception),
        the exception object is returned as an error.
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self._close_connection()
        return result

    def insert_query(self, query):
        """
        Execute an insert SQL query and return None.

        :param query: (list) List that contains sql query itself and queryset from KIS db as a values for our db.
        :return: Result set as a list of tuples.
        In case of an undefined table (UndefinedTable exception),
        the exception object is returned as an error.
        """
        self.cursor.executemany(query[0], query[1])
        self.conn.commit()
        self._close_connection()
        return None

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



