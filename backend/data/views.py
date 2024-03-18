"""This module provide work of main django functions - views."""
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response
from .kis_data import get_chosen_date
from .caching import Cacher


class KISDataReadViewSet(viewsets.ViewSet):

    def list(self, request):
        cached_result = Cacher().main_caching()
        return Response(cached_result)


class KISDataAnotherDates(viewsets.ViewSet):

    def list(self, request):
        result = get_chosen_date(request)
        return Response({'data': result})

