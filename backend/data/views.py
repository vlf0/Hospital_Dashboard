"""This module provide work of main django functions - views."""
from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .kis_data import ensure_cashing
from .serializers import AccumulationOfIncoming, AccumulativeDataSerializer


class KISDataReadViewSet(viewsets.ViewSet):

    def list(self, request):
        ensure_cashing()
        kis = cache.get('kis')
        dmk = cache.get('dmk')
        return Response({'dmk': dmk, 'kis': kis})


