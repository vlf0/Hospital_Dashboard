import random
from types import GeneratorType
from django.test import TestCase
from data.kis_data import (
    KISData,
    QuerySets,
    CleanData,
    DataProcessing,
)


class CleanDataTest(TestCase):

    databases = []

    def test_check_instance_attrs(self) -> None:
        inst = CleanData(first=1, second='true')
        self.assertEqual((inst.first, inst.second), (1, 'true'))


class KISDataTest(TestCase):

    databases = ['kis_db']

    def test_get_data_generator(self) -> None:

        queries = QuerySets()
        generator = KISData(queries.queryset_for_kis()).get_data_generator()
        self.assertIsInstance(generator, GeneratorType)


class DataProcessingTest(TestCase):

    databases = []
    dataset = [
        (1, 'Alice', 'test1', 25),
        (2, 'Bob', 'test2', 40),
        (3, 'Charlie', 'test3', 32)
    ]
    test_cases = [
        {'ind': 1, 'value': 'Bob', 'expected': [(2, 'Bob', 'test2', 40)]},
        {'ind': 1, 'value': 'Dilan', 'expected': []},
        {'ind': 2, 'value': 'test3', 'expected': [(3, 'Charlie', 'test3', 32)]}
    ]

    def test_filter_dataset(self):
        for case in self.test_cases:
            filtered_dataset = DataProcessing.filter_dataset(self.dataset, case['ind'], case['value'])
            self.assertEqual(filtered_dataset, case['expected'])

    def test_slice_dataset(self):
        mapping = {
            'Кардиологическое отделение': 'cardio_d',
            'Хирургическое отделение': 'surgery_d',
            'Терапевтическое отделение': 'therapy_d'
        }
        dataset = [
            ('Хирургическое отделение', 3),
            ('Терапевтическое отделение', 5),
            ('Кардиологическое отделение', 2),
        ]
        case = ['surgery_d', 'therapy_d', 'cardio_d']
        sliced_dataset = DataProcessing.slice_dataset(dataset, mapping)
        self.assertEqual(sliced_dataset[0], case)

    def test_create_instance(self):
        columns = ['id', 'name', 'info', 'age']
        new_instances_list = DataProcessing.create_instance(columns, self.dataset)
        random_instance = random.choice(range(len(new_instances_list)))
        self.assertIsInstance(new_instances_list[random_instance], CleanData)


