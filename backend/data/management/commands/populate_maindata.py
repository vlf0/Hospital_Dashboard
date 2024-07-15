from django.core.management.base import BaseCommand
from data.kis_data import KISData, DataForDMK, MainQueries
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Command for initial collecting and processing data due week and saving to DMK db.'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=7, help='Number of previous days to process')

    def handle(self, *args, **options):
        """Start handling."""
        days = options['days']
        qs = MainQueries()
        dates = self.get_dates(days)
        self.populate_model(dates, qs)

    @staticmethod
    def get_dates(days=7) -> list:
        """Create list of `days` previous dates from today and return its reversed."""
        dates = [date.today()-timedelta(days=day) for day in range(days)]
        dates.reverse()
        return dates

    @staticmethod
    def populate_model(dates: list, queries: MainQueries) -> None:
        """Iterate over dates list, process queries for chosen date and save results to db."""
        for day in dates:
            chosen_date_query = queries.chosen_date_query(queries.create_dmk_query(), day)
            kis_obj = KISData(chosen_date_query)
            DataForDMK(kis_obj).save_to_dmk(day)
