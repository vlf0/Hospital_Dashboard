"""This module provide work of main django functions - views."""
from rest_framework import viewsets
from rest_framework.response import Response
from .caching import Cacher
# from .decorators import main_cache_disable


class KISDataReadViewSet(viewsets.ViewSet):

    # @main_cache_disable
    def list(self, request):
        today_data = Cacher.get_main_cache()
        return Response(today_data)


class KISDataAnotherDates(viewsets.ViewSet):

    def list(self, request):
        cached_result = Cacher.get_chosen_date_cache(request)
        return Response(cached_result)

