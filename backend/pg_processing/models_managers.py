"""Responsible for models managers."""
from django.db import models
from datetime import date, timedelta


class TwoDaysFilterManager(models.Manager):
    """Provide using custom filter method.

    - Custom method: custom_filter() gives 7 last rows from model.
    """

    def custom_filter(self):
        """
        Get 7 last model objects and return as a queryset.

        :return: *list[tuple]* Filtered queryset.
        """
        week_days = [(date.today() - timedelta(days=day)) for day in range(7)]
        return self.filter(dates__in=week_days)
