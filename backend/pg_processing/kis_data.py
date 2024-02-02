"""Responsible for classes defining non-model query-sets from another DB."""
from rest_framework.exceptions import ValidationError
from .psycopg_module import BaseConnectionDB
from .sql_queries import QuerySets
from .serializers import KISDataSerializer, MainDataSerializer
from datetime import date, datetime
import logging

# Local logger config and call
formater = '[%(levelname)s:%(asctime)sms] [Module - %(name)s]\n %(message)s'
logging.basicConfig(filename='pg_processing/pg_logs.log', filemode='w', format=formater, level='INFO')
pg_loger = logging.getLogger(__name__)


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
        self.db_conn = BaseConnectionDB(dbname='postges',
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
    The base class from which other classes are inherited to provide required data
    by adding specific sets of queries.

    Attributes:
      kis_generator: (generator): A generator for retrieving datasets. Must be a KISData instance.

    Methods:
      - error_check(dataset): Check if the dataset contains an error.
      Returns:
      (bool)

      - filter_dataset(dataset, ind, value): Filter dataset based on index and value. Needed for data sorting.
      Returns:
      list): Filtered datasets.

      - count_dataset_total(dataset): Count the total number of rows in the dataset.
      Returns:
      (int):
    """

    def __init__(self, kis_generator):
        """
        Initialize the DataProcessing instance.

        :param kis_generator: (generator): A generator providing datasets.
        """
        self.kis_generator = kis_generator

    @staticmethod
    def error_check(dataset):
        """
        Check if the dataset contains an error.

        :param dataset: (list): The dataset to check.
        :return: bool: True if an error is detected, False otherwise.
        """
        if dataset[0][0] == 'Error':
            return True

    @staticmethod
    def filter_dataset(dataset, ind, value):
        """
        Filter passed dataset based on index and value.

        :param dataset: (list): The dataset to filter.
        :param ind: (int): Index to filter on.
        :param value: Value to match in the filter.
        :return: *list*: Filtered dataset.
        """
        return [row for row in dataset if row[ind] == value]

    @staticmethod
    def count_dataset_total(dataset):
        """
        Count the total number of rows in the dataset.

        :param dataset: (list): The dataset to count.
        :return: *int*: Total number of rows.

        """
        return len(dataset)


class DataForDMK(DataProcessing):
    """
    Class for processing, collecting, and saving data to the DMK DB.

    This class extends the functionality of DataProcessing to handle the process
    of collecting, preparing, and saving data to the DMK database using a generator.

    Attributes:
      kis_generator: (generator): A generator providing datasets.

    Methods:
      - count_data(dataset, ind, value):
        Count total, positive, and negative amounts in the dataset.

      - get_arrived_data() -> dict:
        Get data related to arrivals.

      - get_signout_data() -> dict:
        Get data related to signouts and deaths.

      - get_reanimation_data() -> dict:
        Get data related to reanimation.

      - __collect_data() -> dict:
        Get calculated main values for detail boards on the front-end for saving to DMK DB.

      - save_to_dmk():
        Save the prepared data to the DMK DB using the MainData model and its serializer.

    """

    def __init__(self, kis_generator):
        """
        Initialize the DataForDMK instance, it inherited from parent class.

        Parameters:
          kis_generator (generator): A generator providing datasets.

        """
        super().__init__(kis_generator)

    def count_data(self, dataset, ind, value):
        """
        Count total, positive, and negative amounts in the dataset.

        Negative means refused and deads, and positive means hospitalized and moved to other clinics.

        :param dataset: (list): The dataset to count.
        :param ind: (int): Index to count positive and negative amounts.
        :param value: Value to match in the filter.
        :return: *list*: List containing total, positive, and negative amounts.
        """
        data = self.filter_dataset(dataset, ind, value)
        total_amount = self.count_dataset_total(dataset)
        positive_amount = len(data)
        negative_amount = total_amount - positive_amount
        if ind == 1:
            return [total_amount, negative_amount]
        return [total_amount, positive_amount, negative_amount]

    def get_arrived_data(self) -> dict:
        """
        Get data related to arrivals, hosp and refused patients.

        :return: *dict*: Dictionary containing arrived, hospitalized, and refused data.
        """
        arrived_dataset = next(self.kis_generator)
        result_keys = ['arrived', 'hosp', 'refused']
        if self.error_check(arrived_dataset):
            return dict(zip(result_keys, [None, None, None]))
        ready_values = self.count_data(arrived_dataset, 0, 1)
        return dict(zip(result_keys, ready_values))

    def get_signout_data(self) -> dict:
        """
        Get data related to signouts and deaths patients.

        :return: *dict*: Dictionary containing signout and deaths data.
        """
        arrived_dataset = next(self.kis_generator)
        result_keys = ['signout', 'deads']
        if self.error_check(arrived_dataset):
            return dict(zip(result_keys, [None, None]))
        ready_values = self.count_data(arrived_dataset, 1, 'Другая причина')
        return dict(zip(result_keys, ready_values))

    def get_reanimation_data(self) -> dict:
        """
        Get data related to reanimation patients.

        :return: *dict*: Dictionary containing reanimation data.
        """
        reanimation_dataset = next(self.kis_generator)
        if self.error_check(reanimation_dataset):
            return {'reanimation': None}
        return {'reanimation': self.count_dataset_total(reanimation_dataset)}

    def __collect_data(self) -> dict:
        """
        Get calculated main values for detail boards on the front-end for saving to DMK DB.

        The method calculates data from a set of datasets obtained one by one through iteration of the generator
        and then concatenates it into one common dictionary.

        :return: *dict*: Main data for saving to DMK DB.
        :raises StopIteration: If the generator is already empty. This point also will writen to logs.
        """
        try:
            arrived, signout, deads = self.get_arrived_data(), self.get_signout_data(), self.get_reanimation_data()
            main_data = arrived | signout | deads
            if None in [value for value in main_data.values()]:
                pg_loger.warning(f'[WARNING: {datetime.now()}] Error occurred when data access attempt.'
                                 f' Will writen only NULL values to DMK DB.')
            # Add dates key-value pair to collected data dict.
            today_dict = {'dates': date.today()}
            ready_data = today_dict | main_data
            return ready_data
        except StopIteration:
            pg_loger.error('The generator is already empty. Need re-create KisData object.')

    def save_to_dmk(self):
        """
        Save the prepared data to the DMK DB using the MainData model and its serializer.

        :return: *MainData*: Saved data into the model. If on of the exception will raise - returns nothing.

        :raises ValidationError: If the serializer validation fails.
        :raises SyntaxError: If there is a syntax error in the serializer.
        :raises AssertionError: If there is an assertion error during saving.
        """
        serializer = MainDataSerializer(data=self.__collect_data())
        try:
            serializer.is_valid(raise_exception=True)
            print(serializer.validated_data)
            print([value for value in serializer.validated_data.values()])
            data_instance = serializer.save()
            return data_instance
        except (ValidationError, SyntaxError, AssertionError) as e:
            pg_loger.error(e)
            # return e  # Returns original error text if needed while developing


o = DataForDMK(KISData(QuerySets().queryset_for_dmk()).get_data_generator())


class ArrivedDataProcessing(DataProcessing):

    def __init__(self, dataset):
        super().__init__(dataset)

    def get_datasets_generator(self):
        # Create connect object and generate queries
        data_object = KISData(QuerySets().queryset_for_kis())
        generator = data_object.get_data_generator()
        # Get data-set and give it by command



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