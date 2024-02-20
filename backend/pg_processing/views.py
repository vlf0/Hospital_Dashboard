"""This module provide work of main django functions - views."""
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response
from .kis_data import ensure_cashing


class KISDataReadViewSet(viewsets.ViewSet):

    def list(self, request):
        ensure_cashing()
        kis = cache.get(':1:kis')
        dmk = cache.get(':1:dmk')
        return Response({'dmk': dmk, 'kis': kis})
