"""Responsible for models (tables in DMK BD)."""
from django.db import models
from .models_managers import TwoDaysFilterManager


class MainData(models.Model):
    """Represent table in DMK DB responsible for storage and output data.

    In Meta class defined based B-tree index.
    """
    # Custom manager
    objects = TwoDaysFilterManager()

    dates = models.DateField(unique=True)
    arrived = models.SmallIntegerField(null=True)
    hosp = models.SmallIntegerField(null=True)
    refused = models.SmallIntegerField(null=True)
    signout = models.SmallIntegerField(null=True)
    deads = models.SmallIntegerField(null=True)
    reanimation = models.SmallIntegerField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['dates'])
        ]

