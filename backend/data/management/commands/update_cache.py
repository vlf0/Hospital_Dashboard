from django.core.management.base import BaseCommand
from data.caching import Cacher


class Command(BaseCommand):

    def handle(self, *args, **kwargs) -> None:
        self.update_cache()

    @staticmethod
    def update_cache() -> None:
        Cacher().main_caching()

