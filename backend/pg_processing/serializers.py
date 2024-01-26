"""Responsible for serializers."""
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import MainData
from .psycopg_module import KIS_queryset


class MainDataSerializer(serializers.ModelSerializer):
    """Serialize data of MainData model."""

    class Meta:
        model = MainData
        fields = '__all__'


class KISDataSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    dept = serializers.CharField()
    channel = serializers.CharField()
    patient_type = serializers.CharField()


# data = (2, 'test dept', '103', 'Москва')
kis_data = [(1, 'Неврологическое отделение', 'Самотек', 'ЗЛ'),
            (1, 'ОРИТ №1', '103', 'ЗЛ'),
            (1, 'ОРИТ №2', '103', 'ЗЛ'),
            (1, 'Хирургическое отделение', '103 Поликлиника', 'Иногородний'),
            (1, 'Кардиологическое отделение', '103', 'Иногородний'),
            (1, 'Кардиологическое отделение', '103', 'Иногородний'),
            (1, 'Урологическое отделение', '103', 'Москва'),
            (0, 'ПО', 'Самотек', 'ЗЛ'),
            (0, 'ПО', '103 Поликлиника', 'Москва')]

r_data = []


class Row:

    def __init__(self, id, dept, channel, patient_type):
        self.id = id
        self.dept = dept
        self.channel = channel
        self.patient_type = patient_type



for row in kis_data:
    r_data.append(Row(id=row[0], dept=row[1], channel=row[2], patient_type=row[3]))

print(r_data)

def encode():
    data_sr = KISDataSerializer(r_data, many=True)
    print(data_sr.data)
    json = JSONRenderer().render(data_sr.data).decode(encoding='UTF-8')
    print(json)



# from pg_processing.serializers import encode



