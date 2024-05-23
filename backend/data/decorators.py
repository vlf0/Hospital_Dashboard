"""
Provided functions-decorators for "data" app.
If you don't want using cache system - just add decorator to the viewset.
"""
from rest_framework.response import Response
from .models import MainData
from .serializers import MainDataSerializer
from .kis_data import KISDataProcessing, KISData, QuerySets, DMKManager


def main_cache_disable(func):
    """
    Wrap list  method of main viewset: skip caching and get data by API directly.

    Provided all main data for current date.
    """
    def wrapper(*args, **kwargs):
        main_dmk = MainDataSerializer(MainData.objects.custom_filter(), many=True).data
        accum_dmk = DMKManager.collect_model()
        p_kis = KISDataProcessing(KISData(QuerySets().queryset_for_kis())).create_ready_dicts()
        p_dmk = {'main_dmk': main_dmk, 'accum_dmk': accum_dmk}
        data = {'dmk': p_dmk, 'kis': p_kis}
        return Response(data)
    return wrapper


