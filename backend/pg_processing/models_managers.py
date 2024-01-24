"""Responsible for models managers."""
from django.db import models
from datetime import date, timedelta


class TwoDaysFilterManager(models.Manager):
    """Provide using custom filter method.

    - Custom method: custom_filter() gives 2 last rows only filtered by dates.
    """

    def custom_filter(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        return self.filter(dates__in=[today, yesterday])
