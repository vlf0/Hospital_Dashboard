from .psycopg_module import kis_conn
from .sql_queries import *
from .serializers import KISDataSerializer


class KISData:
    """
    KISData Class

    This class facilitates the creation of a list of CleanData class objects, which can be processed by a DRF serializer.

    Attributes:
    db_conn:  The connection module to the PostgreSQL database.
    cursor:  The method to execute queries on the PostgreSQL database.
    """

    db_conn = kis_conn
    cursor = db_conn.execute_query

    def __init__(self, query_set):
        """
        Initialize an instance of KISData.

        :param query_set: A list containing the query and columns list.
        """
        self.query = query_set[0]
        self.columns_list = query_set[1]

    def count_data(self):
        """
        Retrieve data from the database based on the specified query.

        :return: List of tuples.
        """
        data = self.cursor(self.query)
        return data

    def create_instance(self, target_class):
        """
        Create instances of a target class with data retrieved from the database.

        :param target_class: The class to instantiate for each row.
        :return: List of class instances.
        """
        obj_list = [target_class(**dict(zip(self.columns_list, row))) for row in self.count_data()]
        return obj_list


class CleanData:
    """
    Use this base class for creating defined class objects with passed kwargs.

    When kwargs is passing - they are becoming a new attributes for this class object.
    Designed for creating list of class objects for processing by serializer.
    The attrs of each class object represents column name and its value as a key=value pair
    gotten from KIS DB as a stored info.

    Does not have anything methods..
    """

    def __init__(self, **kwargs):
        """
        Initializes an object with attributes based on key-value pairs provided as keyword arguments.

        :param kwargs: (dict): Keyword arguments representing attribute names and values for the object.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)


