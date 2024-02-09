"""Responsible for classes defining non-model query-sets from another DB."""
from typing import Any, Iterator
from datetime import date, datetime
from collections import Counter
from itertools import chain
import logging
from rest_framework.exceptions import ValidationError
from .psycopg_module import BaseConnectionDB
from .sql_queries import QuerySets
from .serializers import KISDataSerializer, MainDataSerializer, KISTableSerializer


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

    Does not have anything methods.
    """

    def __init__(self, **kwargs):
        """
        Initialize an object with attributes based on key-value pairs provided as keyword arguments.

        :param kwargs: *dict*: Keyword arguments representing attribute names and values for the object.
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
      db_conn:  The connection module to the PostgreSQL database, BaseConnection instance.

      cursor:  The method to execute queries on the PostgreSQL database.

    Methods:
      - get_data_generator -> iterator: Create a generator-iterator object performing each query from queryset by request.
    """

    def __init__(self, query_sets):
        """
        Initialize an instance of KISData.

        :param query_sets: *list*: A list containing the data queries
          and queries of its columns. Each query pair is a list.
        """
        self.query_sets = query_sets
        self.db_conn = BaseConnectionDB(dbname='postgres',
                                        host='localhost',
                                        user='postgres',
                                        password='root'
                                        )
        self.cursor = self.db_conn.execute_query

    def get_data_generator(self) -> Iterator:
        """
        Create an iterator object performing each query from queryset by request.

        Retrieves data from the database based on the specified query passed as a list into init method as arg.

        :return: *Iterator*.
        """
        for dataset in self.query_sets:
            yield self.cursor(dataset[0])
        self.db_conn.close_connection()


class DataProcessing:
    """
    The base class from which other classes are inherited to provide required data by adding specific sets of queries.

    Attributes:
      kis_generator: (Iterator): A generator for retrieving datasets. Must be a KISData instance.

    Methods:
      - error_check(dataset) -> bool: Check if the dataset contains an error.

      - filter_dataset(dataset, ind, value) -> list: Filter dataset based on index and value. Needed for data sorting.

      - count_dataset_total(dataset) -> int: Count the total number of rows in the dataset.
    """

    def __init__(self, kis_generator):
        """
        Initialize the DataProcessing instance.

        :param kis_generator: *iterator*: A generator providing datasets.
        """
        self.kis_generator = kis_generator

    @staticmethod
    def error_check(dataset) -> bool:
        """
        Check if the dataset contains an error.

        :param dataset: *list*: The dataset to check.
        :type dataset: list[tuple]
        :return: *bool*: True if an error is detected, False otherwise.
        """
        if dataset[0][0] == 'Error':
            return True

    @staticmethod
    def filter_dataset(dataset, ind, value) -> list:
        """
        Filter passed dataset based on index and value.

        :param dataset: *list*: The dataset to filter.
        :type dataset: list[tuple]
        :param ind: *int*: Index to filter on.
        :type ind: int
        :param value: *int, str*: Value to match in the filter.
        :type value: int or str
        :return: *list*: Filtered dataset.
        """
        return [row for row in dataset if row[ind] == value]

    @staticmethod
    def count_dataset_total(dataset):
        """
        Count the total number of rows in the dataset.

        :param dataset: *list*: The dataset to count.
        :type dataset: list[tuple]
        :return: *int*: Total number of rows.

        """
        return len(dataset)

    def create_instance(self, columns, dataset) -> list[CleanData]:
        """
        Create instances of a target class with data retrieved from the database.

        :param columns: *list*: A list of column names representing the attributes of the `CleanData` instances.
        :type columns: list[str]
        :param dataset: *list*: A list of lists, where each inner list contains
         data corresponding to a row in the database.
        :type dataset: list[tuple]
        :return: *list[CleanData]*: A list of `CleanData` class instances, each instantiated with data from the provided dataset.
        """
        instances_list = [CleanData(**dict(zip(columns, row))) for row in dataset]
        return instances_list


class DataForDMK(DataProcessing):
    """
    Class for processing, collecting, and saving data to the DMK DB.

    This class extends the functionality of DataProcessing to handle the process
    of collecting, preparing, and saving data to the DMK database using a generator.

    Attributes:
      kis_generator: (iterator): A generator providing datasets.

    Methods:
      - count_data(dataset, ind, value) -> list: Count total, positive, and negative amounts in the dataset.

      - get_arrived_data() -> dict: Get data related to arrivals.

      - get_signout_data() -> dict: Get data related to signouts and deaths.

      - get_reanimation_data() -> dict: Get data related to reanimation.

      - save_to_dmk(): Save the prepared data to the DMK DB using the MainData model and its serializer.
    """

    def __init__(self, kis_generator):
        """
        Initialize the DataForDMK instance, it inherited from parent class.

        :param kis_generator: *iterator*: A generator providing datasets.
        """
        super().__init__(kis_generator)

    def count_data(self, dataset, ind, value) -> list[int]:
        """
        Count total, positive, and negative amounts in the dataset.

        Negative means refused and deads, and positive means hospitalized and moved to other clinics.

        :param dataset: *list*: The dataset to count.
        :type dataset: list[tuple]
        :param ind: *int*: Index to count positive and negative amounts.
        :type ind: int
        :param value: *int, str*: Value to match in the filter.
        :type value: int or str
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
        signout_dataset = next(self.kis_generator)
        result_keys = ['signout', 'deads']
        if self.error_check(signout_dataset):
            return dict(zip(result_keys, [None, None]))
        ready_values = self.count_data(signout_dataset, 1, 'Другая причина')
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
        arrived, signout, deads = self.get_arrived_data(), self.get_signout_data(), self.get_reanimation_data()
        main_data = arrived | signout | deads
        if None in [value for value in main_data.values()]:
            pg_loger.warning(f'[WARNING: {datetime.now()}] Error occurred when data access attempt.'
                             f' Will writen only NULL values to DMK DB.')
        # Add dates key-value pair to collected data dict.
        today_dict = {'dates': date.today()}
        ready_data = today_dict | main_data
        return ready_data

    def save_to_dmk(self):
        """
        Save the prepared data to the DMK DB using the MainData model and its serializer.

        :return: `MainData`: Saved data into the model. If on of the exception will raise - returns nothing and
         write to log file.

        :raises ValidationError: If the serializer validation fails.
        :raises SyntaxError: If there is a syntax error in the serializer.
        :raises AssertionError: If there is an assertion error during saving.
        """
        serializer = MainDataSerializer(data=self.__collect_data())
        try:
            serializer.is_valid(raise_exception=True)
            data_instance = serializer.save()
            return data_instance
        except (ValidationError, SyntaxError, AssertionError) as e:
            pg_loger.error(e)
            # return e  # Returns original error text if needed while developing


class KISDataProcessing(DataProcessing):
    """
    Class contains processing methods for KIS data.

    Used for getting and processing KIS DB data directly.

    Class attributes:
      querysets: QuerySets instance for getting access to its attrs and methods permanent.

    Attributes:
      kis_generator: Iterator: A generator for retrieving datasets. Must be a KISData instance.

    Methods:
      - __count_values(dataset, ind, keywords) -> list[int]: Count values in the dataset based on index and keywords.

      - __result_for_sr(columns, dataset) -> list[CleanData]: Create instances of CleanData with data from the dataset.

      - __serialize(ready_dataset) -> dict: Serialize the processed dataset using the KISDataSerializer.

      - __arrived_process() -> dict: Process and serialize data related to arrivals.

      - __dept_hosp_process() -> dict: Process and serialize data related to departmental hospitals.

      - __signout_process() -> dict: Process and serialize data related to signouts.

      - create_ready_dicts() -> list[dict]: Create a list of dictionaries containing processed and serialized datasets.
    """

    querysets = QuerySets()
    oar_deads_dict = {'oar1': 0, 'oar2': 0, 'oar3': 0}

    def __init__(self, kis_generator):
        """
        Initialize the KISDataProcessing instance.

        :param kis_generator: *iterator*: A generator providing datasets.
        """
        super().__init__(kis_generator)

    def __count_values(self, dataset, ind, keywords) -> list[int]:
        """
        Count values in the dataset based on index and keywords.

        :param dataset: *list*: The dataset to count.
        :type dataset: list[tuple]
        :param ind: *int*: Index to count values.
        :type ind: int
        :param keywords: *list*: Keywords to match in the filter.
        :type keywords: list[str]
        :return: *list[int]*: List containing counted values.
        """
        custom_filter = self.filter_dataset
        grouped_list = [len(custom_filter(dataset, ind, i)) for i in keywords]
        return grouped_list

    @staticmethod
    def __slice_dataset(dataset, mapping) -> list[list]:
        # Creating 1 row inside dataset instead many.
        stacked_tuples_dataset = [tuple(chain.from_iterable(map(tuple, dataset)))]
        # Getting column names from stacked tuple of KIS data.
        ru_columns = list(stacked_tuples_dataset[0][::2])
        # Creating en columns for matching to KIS serializer fields.
        en_columns = [mapping[column] for column in ru_columns]
        # Created dataset manually as list.
        counted_signout_pats = list(stacked_tuples_dataset[0][1::2])
        return [en_columns, counted_signout_pats]

    def __result_for_sr(self, columns, dataset) -> list[CleanData]:
        """
        Create instances of `CleanData` with data from the dataset.

        :param columns: *list*: A list of column names representing the attributes of the `CleanData` instances.
        :type columns: *list[str]*
        :param dataset: *list*: A list of lists, where each inner list contains
         data corresponding to a row in the database.
        :type dataset: *list[tuple]*
        :return: *list[CleanData]*: A list of `CleanData` class instances, each instantiated with
         data from the provided dataset.
        """
        return self.create_instance(columns, dataset)

    @staticmethod
    def __serialize(ready_dataset, data_serializer=True) -> dict:
        """
        Serialize the processed dataset using the KISDataSerializer.

        :param ready_dataset: *list[CleanData]*: The processed dataset.
        :type ready_dataset: list[CleanData]
        :return: *dict*: Serialized data.
        """
        if data_serializer:
            sr_data = KISDataSerializer(ready_dataset, many=True).data
        else:
            sr_data = KISTableSerializer(ready_dataset, many=True).data
        return sr_data

    def __arrived_process(self) -> dict:
        """
        Process and serialize data related to arrivals.

        :return: *dict*: Serialized data.
        """
        querysets = self.querysets
        # Defining columns for serializer and values for filtering datasets.
        columns, channels, statuses = querysets.COLUMNS['arrived'], querysets.channels, querysets.statuses
        # Getting first dataset by generator.
        arrived_dataset = next(self.kis_generator)
        if self.error_check(arrived_dataset):
            sorted_channels_datasets = [0 for cnt in channels]
            sorted_statuses_datasets = [0 for cnt in statuses]
        else:
            hosp_data = self.filter_dataset(arrived_dataset, 0, 1)
            # Calculating channels numbers.
            sorted_channels_datasets = self.__count_values(hosp_data, 2, channels)
            # Calculating patients statuses.
            sorted_statuses_datasets = self.__count_values(hosp_data, -1, statuses)
        # Creating 1 row data in dataset.
        summary_dataset = [tuple(sorted_channels_datasets+sorted_statuses_datasets)]
        ready_dataset = self.__result_for_sr(columns, summary_dataset)
        return self.__serialize(ready_dataset)

    def __dept_hosp_process(self) -> dict:
        """
        Process and serialize data related to hospitalized patients.

         If dataset is the one of postgres errors then create columns list and dataset manually
         that contains all zero to serializer can process it and avoiding errors.

        :return: *dict*: Serialized data.
        """
        pre_dataset = next(self.kis_generator)
        if self.error_check(pre_dataset):
            en_columns = [column for column in self.querysets.profiles_mapping.values()]
            dataset = [tuple([0 for cnt in en_columns])]
        else:
            packed_data = self.__slice_dataset(pre_dataset, self.querysets.profiles_mapping)
            en_columns, dataset = packed_data[0], packed_data[1]
            dataset = [tuple(dataset)]
        ready_dataset = self.__result_for_sr(en_columns, dataset)
        return self.__serialize(ready_dataset)

    def __signout_process(self) -> dict:
        """
        Process and serialize data related to signouts.

        :return: *dict*: Serialized data.
        """
        querysets = self.querysets
        columns, keywords = querysets.COLUMNS['signout'], querysets.signout
        signout_dataset = next(self.kis_generator)
        # Calculating signout from defined depts
        signout_only = self.filter_dataset(signout_dataset, 1, 'Выписан')
        counter = Counter(signout_only)
        counted_signout_dataset = [(dept[0], cnt) for dept, cnt in counter.items()]
        # Preparing data for creating processed dataset
        packed_data = self.__slice_dataset(counted_signout_dataset, querysets.depts_mapping)
        en_columns, dataset = packed_data[0], packed_data[1]
        if self.error_check(signout_dataset):
            sorted_signout_dataset = [0 for cnt in columns]
        else:
            sorted_signout_dataset = self.__count_values(signout_dataset, 1, keywords)
        summary_dataset = [tuple(sorted_signout_dataset + dataset)]
        summary_columns = columns + en_columns
        ready_dataset = self.__result_for_sr(summary_columns, summary_dataset)
        return self.__serialize(ready_dataset)
    
    def __deads_process(self):
        """
        Process and serialize data related to signouts.

        :return:
        """
        deads_dataset = next(self.kis_generator)
        # Counting deads patients in OARs
        oars_filtered = [row for row in deads_dataset if row[6] in ['ОРИТ №1', 'ОРИТ №2', 'ОРИТ №3']]
        counter = Counter(oars_filtered)
        counted_oars_deads = [[oar[6], cnt] for oar, cnt in counter.items()]
        # Creating dict for updating class attr for further using in OARs table-data processing
        deads_dict = {self.querysets.depts_mapping[oar[0]]: oar[1] for oar in counted_oars_deads}
        self.oar_deads_dict.update(deads_dict)
        print(self.oar_deads_dict)
        # Processing table data for serializing.
        columns = BaseConnectionDB(dbname='postgres',
                                   host='localhost',
                                   user='postgres',
                                   password='root',
                                   auto_close=True
                                   ).execute_query(self.querysets.COLUMNS['deads_t'])
        stacked_columns = list(chain.from_iterable(map(tuple, columns)))
        ready_dataset = self.__result_for_sr(stacked_columns, deads_dataset)
        return self.__serialize(ready_dataset, data_serializer=False)


    def create_ready_dicts(self) -> list[dict]:
        """
        Create a list of dictionaries containing processed and serialized datasets.

        :return: *list[dict]*: List of dictionaries containing processed and serialized datasets.
        """
        keywords = self.querysets.DICT_KEYWORDS
        arrived = self.__arrived_process()
        hosp_dept = self.__dept_hosp_process()
        signout = self.__signout_process()
        deads = self.__deads_process()
        # Creating list of ready processed datasets.
        ready_dataset = [arrived, hosp_dept, signout, deads]
        # Creating list of dicts where keys takes from query class
        # and values are ready dataset iterating list of them one by one.
        result = [{keywords[ready_dataset.index(dataset)]: dataset for dataset in ready_dataset}]
        return result

