"""Responsible for classes defining non-model query-sets from another DB."""
from rest_framework.exceptions import ValidationError
from .psycopg_module import BaseConnectionDB
from .sql_queries import QuerySets
from .serializers import KISDataSerializer, MainDataSerializer
from datetime import date


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

    def __init__(self, query_sets):
        """
        Initialize an instance of KISData.

        :param query_sets: A list containing the data queries and queries of its columns. Each query pair is a list.
        """
        self.query_sets = query_sets
        self.db_conn = BaseConnectionDB(dbname='postgres',
                                        host='localhost',
                                        user='postgres',
                                        password='root'
                                        )
        self.cursor = self.db_conn.execute_query

    def get_data_generator(self):
        """
        Create a generator-iterator object performing each query from queryset by request.

        Retrieves data from the database based on the specified query passed as a list into init method as arg.

        :return: List of tuples.
        """
        for dataset in self.query_sets:
            yield self.cursor(dataset[0])
        self.db_conn.close_connection()

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
    #     generator = self.get_data_generator()
    #     columns, data = next(generator), next(generator)
    #     instances_list = [target_class(**dict(zip(columns, row))) for row in data]
    #     return instances_list


class DataProcessing:
    """
    The base class from which other classes are inherited and its functionality is taken.

    This class provides the required set of data by adding specific sets of queries.

    """

    def __init__(self, kis_generator):
        self.kis_generator = kis_generator

    @staticmethod
    def error_check(dataset):
        if dataset[0][0] == 'Error':
            return True

    @staticmethod
    def filter_dataset(dataset, ind, value):
        return [row for row in dataset if row[ind] == value]

    @staticmethod
    def count_dataset_total(dataset):
        return len(dataset)


class DataForDMK(DataProcessing):
    """
    Class for getting, preparing, and saving data to DMK DB.

    This class is designed to handle the process of collecting, preparing, and saving data to the DMK database.
    It uses a generator to retrieve datasets from another database, processes the data, and then saves it to
    the DMK DB using the MainData model.

    Methods:

    - collect_data(): Retrieves and calculates main values for detail boards on the front-end.
      The method calculates data from a set of datasets obtained one by one through iteration of the generator
      and then concatenates it into one common dictionary.

      Returns:
      dict: Main data for saving to DMK DB.


    - add_data(): Prepare data for saving by adding date information to the collected data.

      Returns:
      dict: Ready data for saving to DMK DB.


    - save_to_dmk(): Save the prepared data to the DMK DB using the MainData model.

      Returns:
      MainData: Saved data.

    """

    def __init__(self, kis_generator):
        super().__init__(kis_generator)

    def count_data(self, dataset, ind, value):

        data = self.filter_dataset(dataset, ind, value)
        total_amount = self.count_dataset_total(dataset)
        positive_amount = len(data)
        negative_amount = total_amount - positive_amount
        if ind == 1:
            return [total_amount, negative_amount]
        return [total_amount, positive_amount, negative_amount]

    def get_arrived_data(self) -> dict:
        arrived_dataset = next(self.kis_generator)
        result_keys = ['arrived', 'hosp', 'refused']
        if self.error_check(arrived_dataset):
            return dict(zip(result_keys, [None, None, None]))
        ready_values = self.count_data(arrived_dataset, 0, 1)
        return dict(zip(result_keys, ready_values))

    def get_signout_data(self) -> dict:
        arrived_dataset = next(self.kis_generator)
        result_keys = ['signout', 'deads']
        if self.error_check(arrived_dataset):
            return dict(zip(result_keys, [None, None]))
        ready_values = self.count_data(arrived_dataset, 1, 'Другая причина')
        return dict(zip(result_keys, ready_values))

    def get_reanimation_data(self) -> dict:
        reanimation_dataset = next(self.kis_generator)
        if self.error_check(reanimation_dataset):
            return {'reanimation': None}
        return {'reanimation': self.count_dataset_total(reanimation_dataset)}

    def collect_data(self) -> dict:
        """
        Get calculated main values for detail boards on the front-end for saving to DMK DB.

        The method calculates data from a set of datasets obtained one by one through iteration of the generator
        and then concatenates it into one common dictionary.

        :return: *dict*: Main data for saving to DMK DB.
        """
        arrived, signout, deads = self.get_arrived_data(), self.get_signout_data(), self.get_reanimation_data()
        main_data = arrived | signout | deads
        # Add dates key-value pair to collected data dict.
        today_dict = {'dates': date.today()}
        ready_data = today_dict | main_data
        return ready_data

    def save_to_dmk(self):
        """
        Save the prepared data to the DMK DB using the MainData model and its serializer.

        :return: *MainData*: Saved data into model. If error - not save data to DMK and return None.
        """
        serializer = MainDataSerializer(data=self.collect_data())
        try:
            serializer.is_valid(raise_exception=True)
            return serializer.save()
        except ValidationError as e:
#TODO need to implement logger here to write access attempts to DMK twice per one day.
            return


o = DataForDMK(KISData(QuerySets().queryset_for_dmk()).get_data_generator())


class ArrivedDataProcessing(DataProcessing):

    def __init__(self, dataset):
        super().__init__(dataset)

    def get_datasets_generator(self):
        # Create connect object and generate queries
        data_object = KISData(QuerySets().queryset_for_kis())
        generator = data_object.get_data_generator()
        # Get data-set and give it by command
        first_dataset = DataProcessing(next(generator))
        yield first_dataset
        second_dataset = DataProcessing(next(generator))
        yield second_dataset
        third_dataset = DataProcessing(next(generator))
        yield third_dataset
        fourth_dataset = DataProcessing(next(generator))
        yield fourth_dataset
        fifth_dataset = DataProcessing(next(generator))
        yield fifth_dataset
        sixth_dataset = DataProcessing(next(generator))
        yield sixth_dataset


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


# o = DataProcessing().get_datasets_generator(KISData(QuerySets().queryset_for_dmk()))
# o = kis_data.DataProcessing().get_datasets_generator(kis_data.KISData(kis_data.QuerySets().queryset_for_dmk()))
k = KISData(QuerySets().queryset_for_dmk())

s = KISData(QuerySets().queryset_for_kis())