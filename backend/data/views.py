"""This module provide work of main django functions - views."""
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response
from .kis_data import ensure_cashing, get_chosen_date


class KISDataReadViewSet(viewsets.ViewSet):

    def list(self, request):
        ensure_cashing()
        kis = cache.get('kis')
        dmk = cache.get('dmk')
        return Response({'dmk': dmk, 'kis': kis})


class KISDataAnotherDates(viewsets.ViewSet):

    def list(self, request):
        print(request.query_params)
        result = get_chosen_date(request)
        return Response({'data': result})

