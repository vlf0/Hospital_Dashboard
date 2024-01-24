"""Responsible for models managers."""
from django.db import models
from datetime import date, timedelta


class TwoDaysFilterManager(models.Manager):
    """Provide using custom filter method.

    - Custom method: custom_filter() gives 2 last rows only filtered by dates.
    """

    def custom_filter(self):
        """Filter last 7 rows from queryset using __in filter method and list comprehension."""
        week_days = [(date.today() - timedelta(days=day)) for day in range(7)]
        return self.filter(dates__in=week_days)
