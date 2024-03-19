from django.core.cache import cache
from .kis_data import QuerySets, KISData, KISDataProcessing, collect_model, get_chosen_date
from .serializers import MainDataSerializer
from .models import MainData


class Cacher:

    @staticmethod
    def dmk_cache() -> None:
        if cache.get('dmk') is None:
            main_dmk = MainDataSerializer(MainData.objects.custom_filter(), many=True).data
            accum_dmk = collect_model()
            dmk = {'main_dmk': main_dmk, 'accum_dmk': accum_dmk}
            cache.set('dmk', dmk)

    @staticmethod
    def kis_cache() -> None:
        if cache.get('kis') is None:
            p_kis = KISDataProcessing(KISData(QuerySets().queryset_for_kis())).create_ready_dicts()
            cache.set('kis', p_kis)

    @staticmethod
    def additional_caching(request):
        kind = request.query_params.get('type', None)
        dates = request.query_params.get('date', None)
        if cache.get(f'{kind}_{dates}') is None:
            result_dict = get_chosen_date(kind, dates)
            cache.set(f'{kind}_{dates}', result_dict)
            additional_kis = cache.get(f'{kind}_{dates}')
            return {f'{kind}_{dates}': additional_kis}

    def main_caching(self) -> dict:
        """
        Check redis cash and write data into if storage is empty.

         We are calling this func in the main view to avoid unnecessary calls to the database.
         First call of the day provides writing data into cache and use
         the cache during the day new call to db instead.
        """
        self.dmk_cache()
        self.kis_cache()
        dmk = cache.get('dmk')
        kis = cache.get('kis')
        return {'dmk': dmk, 'kis': kis}




