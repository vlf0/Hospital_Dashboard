"""This module provide work of main django functions - views."""
from rest_framework import viewsets
from rest_framework.response import Response
from .caching import Cacher
from .decorators import main_cache_disable, additional_cache_disable


class KISDataReadViewSet(viewsets.ViewSet):

    @main_cache_disable
    def list(self, request):
        cached_result = Cacher().main_caching()
        return Response(cached_result)


class KISDataAnotherDates(viewsets.ViewSet):

    @additional_cache_disable
    def list(self, request):
        cached_result = Cacher.additional_caching(request)
        return Response(cached_result)

