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
        self.db_conn.close_connection()

    # def get_dmk_data(self):
    #     """Get calculated main values for detail boards on front-end to rather save them into DMK DB."""
    #
    #     return

    def create_instance(self, target_class):
        """
        Create instances of a target class with data retrieved from the database.

        :param target_class: The class to instantiate for each row.
        :return: List of class instances.
        """
        if self.db_conn.error:
            # List of one class with error text
            return [CleanData(error=self.db_conn.error)]
        generator = self.get_data_generator()
        columns, data = next(generator), next(generator)
        instances_list = [target_class(**dict(zip(columns, row))) for row in data]
        return instances_list


kis_data_object = KISData(QuerySets().get_ready_queryset())


class DataForDMK:

    @staticmethod
    def get_datasets_generator():
        generator = kis_data_object.get_data_generator()
        arrived_dataset = ArrivedDataProcessing(next(generator))
        yield arrived_dataset
        signout_dataset = SignOutDataProcessing(next(generator))
        yield signout_dataset
        deads_dataset = next(generator)
        yield deads_dataset
        reanimation_dataset = next(generator)
        yield reanimation_dataset

    def collect_data(self):
        generator = self.get_datasets_generator()
        arrived_data = next(generator).data_to_dmk()
        signout_data = next(generator).data_to_dmk()
        return arrived_data | signout_data


class DataProcessing:

    error = False
    total_amount = 0

    def __init__(self, dataset):
        self.dataset = dataset
        self.error = True if self.dataset[0][0] == 'Error' else False
        self.__define_amounts_attrs()

    def __define_amounts_attrs(self):
        if not self.error:
            self.total_amount = len(self.dataset)

    def filter_dataset(self, ind, value):
        return [row for row in self.dataset if row[ind] == value]


class ArrivedDataProcessing(DataProcessing):

    def __init__(self, dataset):
        super().__init__(dataset)

    def data_to_dmk(self):
        hosp_data = self.filter_dataset(0, 1)
        hosp_amount = len(hosp_data)
        refused_amount = self.total_amount - hosp_amount
        arrived_set = {'arrived': self.total_amount, 'hosp': hosp_amount, 'refused': refused_amount}
        return arrived_set

    # def arrived_process(self):
    #     custom_filter = self.filter_dataset
    #     hosp_data = self.filter_dataset(self.dataset, 0, 1)
    #     singly = custom_filter(hosp_data, 2, 'Самотек')
    #     clinic_103 = custom_filter(hosp_data, 2, '103 Поликлиника')
    #     only_clinic = custom_filter(hosp_data, 2, 'Поликлиника')
    #     only_103 = custom_filter(hosp_data, 2, '103')
    #     t = list(map(len, (singly, clinic_103, only_clinic, only_103)))
    #     return t


class SignOutDataProcessing(ArrivedDataProcessing):

    def __init__(self, dataset):
        super().__init__(dataset)

    def data_to_dmk(self):
        signout_data = self.filter_dataset(1, 'Другая причина')
        signout_amount = len(signout_data)
        deads_amount = self.total_amount - signout_amount
        signout_set = {'signout': self.total_amount, 'deads': deads_amount}
        return signout_set


q = DataForDMK().collect_data()
print(q)

sr = KISDataSerializer


