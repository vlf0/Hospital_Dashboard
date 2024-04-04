from django.db import models


class KISProfiles(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'profile_med'
        managed = False
