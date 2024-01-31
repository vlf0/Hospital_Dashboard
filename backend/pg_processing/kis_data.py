"""Responsible for classes defining non-model query-sets from another DB."""
from .psycopg_module import BaseConnectionDB
from .sql_queries import QuerySets
from .serializers import KISDataSerializer

kis_conn = BaseConnectionDB(dbname='postgres',
                            host='localhost',
                            user='postgres',
                            password='root'
                            )


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
        Initialize an object with attributes based on key-value pairs provided as keyword arguments.

        :param kwargs: (dict): Keyword arguments representing attribute names and values for the object.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)


class KISData:
    """
    KISData class.

    This class facilitates the creation of a generator-iterator object for retrieving data from the PostgreSQL database
    using a series of queries specified in the query_sets attribute. Each query pair in query_sets is a list containing
    the data query and its corresponding column queries.

    Attributes:
    db_conn:  The connection module to the PostgreSQL database.
    cursor:  The method to execute queries on the PostgreSQL database.
    """

    db_conn = kis_conn
    cursor = db_conn.execute_query

    def __init__(self, query_sets):
        """
        Initialize an instance of KISData.

        :param query_sets: A list containing the data queries and queries of its columns. Each query pair is a list.
        """
        self.query_sets = query_sets

    def get_data_generator(self):
        """
        Create a generator-iterator object performing each query from queryset by request.

        Retrieves data from the database based on the specified query passed as a list into init method as arg.

        :return: List of tuples.
        """
        for dataset in self.query_sets:
            yield self.cursor(dataset[0])

    # def create_instance(self, target_class):
    #     """
    #     Create instances of a target class with data retrieved from the database.
    #
    #     :param target_class: The class to instantiate for each row.
    #     :return: List of class instances.
    #     """
    #     if self.db_conn.error:
    #         # List of one class with error text
    #         return [CleanData(error=self.db_conn.error)]
    #     instances_list = [target_class(**dict(zip(self.columns_list, row))) for row in self.get_data()]
    #     return instances_list

