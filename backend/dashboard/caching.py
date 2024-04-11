"""Provided class """
from django.core.cache import cache
from .kis_data import QuerySets, KISData, KISDataProcessing, collect_model
from .serializers import MainDataSerializer
from .models import MainData


class Cacher:
    """Utility class for caching data to improve performance by reducing database queries."""

    @staticmethod
    def dmk_cache() -> None:
        """
        Cache main DMK data.

        Retrieves main DMK data from the database, serializes it, and stores it in the cache.
        """
        main_dmk = MainDataSerializer(MainData.objects.custom_filter(), many=True).data
        accum_dmk = collect_model()
        dmk = {'main_dmk': main_dmk, 'accum_dmk': accum_dmk}
        cache.set('dmk', dmk)

    @staticmethod
    def kis_cache() -> None:
        """
        Cache KIS data.

        Processes data from KIS DB, creates ready dictionaries, and stores them in the cache.
        """
        p_kis = KISDataProcessing(KISData(QuerySets().queryset_for_kis())).create_ready_dicts()
        cache.set('kis', p_kis)

    @staticmethod
    def week_kis_cache() -> None:
        """
        Cache weekly KIS data.

        Retrieves weekly KIS data for arrivals and signouts, combines them into a common dictionary,
        and stores each row in the cache.
        """
        q = QuerySets
        arrived = KISDataProcessing.get_week_kis_data(q.ARRIVED, 'arrived')
        signout = KISDataProcessing.get_week_kis_data(q.SIGNOUT, 'signout')
        common_dict = arrived | signout
        for row in common_dict.items():
            cache.set(f'{row[0]}', row[1])

    def main_caching(self) -> None:
        """
        Cache main data.

        Calls all static methods to set ready data to cache.
        """
        self.dmk_cache()
        self.kis_cache()
        self.week_kis_cache()

    @staticmethod
    def get_chosen_date_cache(request):
        kind = request.query_params.get('type', None)
        dates = request.query_params.get('date', None)
        result = cache.get(f'{kind}_{dates}')
        return result

    @staticmethod
    def get_main_cache():
        dmk, kis = cache.get('dmk'), cache.get('kis')
        today_data = {'dmk': dmk, 'kis': kis}
        return today_data



