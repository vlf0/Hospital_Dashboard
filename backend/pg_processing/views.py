"""This module provide work of main django functions - views."""
from django.db.models.query import QuerySet
from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response
from .models import MainData
from .serializers import MainDataSerializer as DMK_Sr
from .kis_data import KISData, KISDataProcessing, QuerySets


class MainDataReadViewSet(viewsets.ReadOnlyModelViewSet,
                          mixins.CreateModelMixin):
    """Allow access to read main data from DMK DB by using GET method only."""

    queryset = MainData.objects.custom_filter()
    serializer_class = DMK_Sr


class KISDataReadViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = KISDataProcessing(KISData(QuerySets().queryset_for_kis()).get_data_generator()).create_ready_dicts()
        print(queryset)
        return Response(queryset)
