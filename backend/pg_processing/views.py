"""This module provide work of main django functions - views."""
from rest_framework import viewsets
from rest_framework.response import Response
from .models import MainData
from .serializers import MainDataSerializer as DMK_Sr
from .kis_data import KISData, KISDataProcessing, QuerySets


class KISDataReadViewSet(viewsets.ViewSet):

    def list(self, request):
        kis = KISDataProcessing(KISData(QuerySets().queryset_for_kis())).create_ready_dicts()
        dmk = DMK_Sr(MainData.objects.custom_filter(), many=True).data
        return Response({'dmk': dmk, 'kis': kis})
