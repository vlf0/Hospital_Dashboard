"""Describes connection and sql queries to Postgres DB."""
import logging
from typing import Any
from psycopg2 import OperationalError, ProgrammingError
from psycopg2.errors import UndefinedTable, SyntaxError, InFailedSqlTransaction
import psycopg2

logger = logging.getLogger('data.psycopg_module.BaseConnectionDB')


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
    - user(str): The username for the database connection.
    - password(str): The password for the database connection.
    - dbname(str): The name of the database.
    - host(str): The host address of the database.
    - port(int): The port number for the database connection. Defaults to 5432.
    - auto_close(bool): Define whether the connection closes after each transaction.
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

    def __str__(self) -> str:
        """
        Represent connection object as a string.

         If obj is None - it means that connection is not established and was got error.
         Otherwise, represents connection object.

        :return: *str*
        """
        return f'{self.conn}'

    def __connect(self) -> None:
        """
        Private method to establish a database connection.

         A valid psycopg2 connection object sets as a class attribute "conn" if the connection is successful.
         If an error occurs during connection, error instance sets as an "error" class attribute.
        """
        try:
            self.conn = psycopg2.connect(user=self.user, password=self.password,
                                         dbname=self.dbname, host=self.host, port=self.port)
        except (OperationalError, UnicodeDecodeError,
                SyntaxError, ProgrammingError) as connection_error:
            self.error = connection_error
            logger.error(str(self.error).rstrip('\n'))

    def close_connection(self) -> None:
        """Save commits and close the database connection and all its cursors."""
        if self.conn is not None:
            self.conn.close()

    @property
    def connection_status(self) -> Any:
        """
        Read-only property represent boll status in integer format.

        :return: *int*: Connection status. If return "0" - connection is opened now.
         If "1" - connection is already closed. If "-2" - was not opened or closed with error.
        """
        if self.error is not None:
            return -2, self.error
        return self.conn.closed

    def execute_query(self, query, insert=False):
        """
        Execute a SQL query.

        :param query: *str*: The SQL query to be executed.
        :param insert: Bool value response for fetching result of query if it is.
        :return: *list*: The result of the query execution - list of tuples.
        """
        if self.error:
            return [('Error', self.error)]
        cursor = self.conn.cursor()
        if insert:
            self.__execute_insert(query, cursor)
            self.conn.commit()
            return
        result = self.__execute_get(query, cursor)
        if self.auto_close:
            self.close_connection()
        cursor.close()
        return result

    @staticmethod
    def __execute_get(query, cursor) -> list:
        """
        Execute a SQL SELECT query and return the result set getting all rows.

        :param query: *str*: The SQL SELECT query to be executed.
        :type query: str

        :return: *list*: Result set as a list of tuples.
        """
        try:
            cursor.execute(query)
            queryset = cursor.fetchall()
            return queryset
        except (ProgrammingError, UndefinedTable) as e:
            print(e)
            pass

    def __execute_insert(self, query: str, cursor) -> None:
        try:
            cursor.execute(query)
            self.conn.commit()
        except InFailedSqlTransaction as e:
            self.conn.rollback()

    @property
    def get_connection_data(self):
        """
        Get the connection parameters of the database.

        :return: *dict*: Dictionary containing database connection parameters.
        """
        return {
            'dbname': self.dbname,
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password
        }


