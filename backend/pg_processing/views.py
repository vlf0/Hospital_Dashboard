"""This module provide work of main django functions - views."""
from django.db.models.query import QuerySet
from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response
from .models import MainData
from .serializers import MainDataSerializer as DMK_Sr
from .kis_data import KISData, KISDataProcessing, QuerySets


class KISDataReadViewSet(viewsets.ViewSet):

    def list(self, request):
        dmk = DMK_Sr(MainData.objects.custom_filter(), many=True).data
        kis = KISDataProcessing(KISData(QuerySets().queryset_for_kis()).get_data_generator()).create_ready_dicts()
        return Response({'dmk': dmk, 'kis': kis})
