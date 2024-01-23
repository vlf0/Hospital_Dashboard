from django.db import models


class MainData(models.Model):
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


