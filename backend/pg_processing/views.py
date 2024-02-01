"""This module provide work of main django functions - views."""
from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response
from .models import MainData
from .serializers import MainDataSerializer, KISDataSerializer
from .kis_data import DataForDMK


class MainDataReadViewSet(viewsets.ReadOnlyModelViewSet):
    """Allow access to read main data from DMK DB by using GET method only."""

    queryset = MainData.objects.custom_filter()
    serializer_class = MainDataSerializer


class KISDataReadViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = 1
        serializer = KISDataSerializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)
