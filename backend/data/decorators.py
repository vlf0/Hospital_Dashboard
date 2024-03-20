"""Provided functions-decorators for "data" app."""
from rest_framework.response import Response
from .models import MainData
from .serializers import MainDataSerializer
from .kis_data import KISDataProcessing, KISData, QuerySets, collect_model, get_chosen_date


def main_cache_disable(func):
    """
    Wrap list  method of main viewset: skip caching and get data by API directly.

    Provided all main data for current date.
    """
    def wrapper(*args, **kwargs):
        main_dmk = MainDataSerializer(MainData.objects.custom_filter(), many=True).data
        accum_dmk = collect_model()
        p_kis = KISDataProcessing(KISData(QuerySets().queryset_for_kis())).create_ready_dicts()
        p_dmk = {'main_dmk': main_dmk, 'accum_dmk': accum_dmk}
        data = {'dmk': p_dmk, 'kis': p_kis}
        return Response(data)
    return wrapper


def additional_cache_disable(func):
    """
    Wrap list method of second additional viewset: skip caching and get data by API directly.

    Provided kis data for chosen date.
    """
    def wrapper(*args, **kwargs):
        kind = args[1].query_params.get('type', None)
        dates = args[1].query_params.get('date', None)
        result_dict = get_chosen_date(kind, dates)
        data = {f'{kind}_{dates}': result_dict}
        return Response(data)
    return wrapper
