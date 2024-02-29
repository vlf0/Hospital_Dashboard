"""Responsible for models (tables in DMK BD)."""
from django.db import models
from .models_managers import CustomManager


class MainData(models.Model):
    """Represent table in DMK DB responsible for storage and output data.

    In Meta class defined based B-tree index.
    """
    # Custom manager
    objects = CustomManager()

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


class AccumulationOfIncoming(models.Model):
    """
    Represent table contains data of incoming patients sorted by depts.

    Accumulates data every day and gives them by request.
    """
    # Custom manager
    objects = CustomManager()

    dates = models.DateField(unique=True)
    therapy = models.CharField(max_length=50, null=True)
    surgery = models.CharField(max_length=50, null=True)
    cardiology = models.CharField(max_length=50, null=True)
    urology = models.CharField(max_length=50, null=True)
    neurology = models.CharField(max_length=50, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['dates'])
        ]

