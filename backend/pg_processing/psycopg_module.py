#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Describes connection and sql queries to Postgres DB."""

from psycopg2 import OperationalError, ProgrammingError, extensions
from psycopg2.errors import UndefinedTable, SyntaxError
import psycopg2
import logging


# Local logger config and call
formater = '[%(levelname)s:%(asctime)sms] [Module - %(name)s]\n %(message)s'
logging.basicConfig(filename='pg_logs.log', filemode='w', format=formater)
pg_loger = logging.getLogger(__name__)


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
    - user (str): The username for the database connection.
    - password (str): The password for the database connection.
    - dbname (str): The name of the database.
    - host (str): The host address of the database.
    - port (int): The port number for the database connection. Defaults to 5432.
    - auto_close (bool): Define whether the connection closes after each transaction.
      If True, all cursors and connection will be closed automatically; no need to call close_connection() method.
      By default, False is configured.
    """

    def __init__(self, user, password, dbname, host, port=5432, auto_close=False):
        """
        Pass the connection values to the database you need.

        :param user: The username for the database connection. Defaults to 'postgres'.
        :param password: The password for the database connection. Defaults to 'root'.
        :param dbname: The name of the database. Defaults to 'postgres'.
        :param host: The host address of the database. Defaults to 'localhost'.
        :param port: The port number for the database connection. Defaults to 5432.
        :param auto_close: Define whether the connection closes after each transaction.
                          If True, all cursors and connection will be closed automatically;
                          no need to call close_connection() method. Defaults to False.
        """
        self.user = user
        self.password = password
        self.dbname = dbname
        self.host = host
        self.port = port
        self.auto_close = auto_close
        self.conn = None
        self.error = None
        self.__connect()

    # Private method that trying to establish connection and set result in class attribute.
    def __connect(self):
        """
        Private method to establish a database connection.

        :return: (psycopg2.extensions.connection) A valid psycopg2 connection object if the connection is successful.
                 If an error occurs during connection, the method returns the specific exception instance
                 (OperationalError or UnicodeDecodeError).
        """
        try:
            self.conn = psycopg2.connect(user=self.user, password=self.password,
                                         dbname=self.dbname, host=self.host, port=self.port)
        except (OperationalError, UnicodeDecodeError, UndefinedTable,
                SyntaxError, ProgrammingError) as connection_error:
            self.error = connection_error
            pg_loger.error(self.error)

    def close_connection(self):
        """
        Save commits and close the database connection and all its cursors.

        :return: None
        """
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()

    @property
    def connection_status(self):
        """
        Read-only property represent boll status in integer format.

        :return: (int): Connection status. If return "0" - connection is opened now.
        If "1" - connection is already closed. If "-2" - connection is already closed.
        """
        if self.error is not None:
            # -2 - custom error code telling about connection was not established
            return -2, self.error
        return self.conn.closed

    def execute_query(self, query, insert_data=None):
        """
        Execute a SQL query.

        :param query: (str): The SQL query to be executed.
        :param insert_data: (list): Data to be inserted if provided for insert query.
               When is provided will be executed inserting query and simple get query if not. Defaults to None.

        :return: (list) The result of the query execution - list of tuples.
                 ()
                 (None) If insert_data was provided then executing insert query. In this case function returns None
                 because we get nothing from DB, insert only.
        """
        if insert_data:
            if self.error:
                self.__execute_insert(query, insert_data)
            self.__execute_insert(query, insert_data)
            return
        # Return list of ine tuple containing error text to any sql query if connection was not established
        if self.error:
            return [('Error', self.error)]

        result = self.__execute_get(query)
        if self.auto_close:
            self.close_connection()
        return result

    def __execute_get(self, query):
        """
        Execute a SQL SELECT query and return the result set.

        :param query: (str): The SQL SELECT query to be executed.

        :return: (list) Result set as a list of tuples.
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        queryset = cursor.fetchall()
        return queryset

    def __execute_insert(self, query, insert_data):
        """
        Execute a SQL INSERT query.

        Args:
        :param query: (str): The SQL INSERT query to be executed.
        :param insert_data: (list): Data to be inserted.

        :return: None
        """
        cursor = self.conn.cursor()
        cursor.executemany(query, insert_data)
        self.close_connection()

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



