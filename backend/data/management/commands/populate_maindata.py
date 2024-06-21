from django.core.management.base import BaseCommand
from data.kis_data import KISData, DataForDMK, QuerySets
from datetime import date, timedelta


class Command(BaseCommand):
    """
    Command for initial collecting and processing data due week and saving to DMK db.

    Can use if the app runnig first time and also for version of the app deployed in Docker
    (because every runnig in docker will create all services from scratch, so DB will be emtpy).
    """

    def handle(self, *args, **kwargs) -> None:
        """Start handling."""
        qs = QuerySets()
        dates = self.get_dates()
        self.populate_model(dates, qs)

    @staticmethod
    def get_dates() -> list:
        """Create list of 7 previous dates from today and return its reversed."""
        dates = [date.today()-timedelta(days=day) for day in range(7)]
        dates.reverse()
        return dates

    @staticmethod
    def populate_model(dates: list, queries: QuerySets) -> None:
        """Iterate over dates list, process queries for chosen date and save results to db."""
        for day in dates:
            chosen_date_query = queries.chosen_date_query(queries.queryset_for_dmk(), day)
            kis_obj = KISData(chosen_date_query)
            DataForDMK(kis_obj).save_to_dmk(day)


