from django.core.management.base import BaseCommand
from data.caching import Cacher


class Command(BaseCommand):
    """
    Class for updating all main cache.

    It is not change already existing data in DMK db, just takes this data.
    From KIS db it takes data too, but after performing update of cache
    they can be different with already gotten KIS data before
    (because data in KIS db is not fixed data and can be changed during the day).
    """
    def handle(self, *args, **kwargs) -> None:
        """Start handling."""
        self.update_cache()

    @staticmethod
    def update_cache() -> None:
        Cacher().main_caching()

