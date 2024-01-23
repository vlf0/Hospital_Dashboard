"""Responsible for models (tables in DMK BD)."""
from django.urls import path, include
from django.db import models


class MainData(models.Model):
    """Represent table in DMK DB responsible for storage and output data.

    In Meta class defined based B-tree index.
    """

    id = models.IntegerField(primary_key=True)
    dates = models.DateField(unique=True)
    arrived = models.SmallIntegerField()
    hosp = models.SmallIntegerField()
    refused = models.SmallIntegerField()
    signout = models.SmallIntegerField()
    deads = models.SmallIntegerField()
    reanimation = models.SmallIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['dates'])
        ]


