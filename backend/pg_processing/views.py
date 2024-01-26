"""This module provide work of main django functions - views."""
from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response
from .models import MainData
from .serializers import MainDataSerializer, KISDataSerializer
from .psycopg_module import KIS_queryset


class MainDataReadViewSet(viewsets.ReadOnlyModelViewSet):
    """Allow access to read main data from DMK DB by using GET method only."""

    queryset = MainData.objects.custom_filter()
    serializer_class = MainDataSerializer


data = (2, 'test dept', '103', 'Москва')


class Row:

    def __init__(self, id, dept, channel, patient_type):
        self.id = id
        self.dept = dept
        self.channel = channel
        self.patient_type = patient_type


r = [
     Row(id=data[0], dept=data[1], channel=data[2], patient_type=data[3]),
     Row(id=data[0], dept=data[1], channel=data[2], patient_type=data[3])
    ]

class KISDataReadViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = r
        serializer = KISDataSerializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)





