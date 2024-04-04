from django.db import models


class KISProfiles(models.Model):

    name = models.CharField(max_length=255, verbose_name='Название профиля')

    class Meta:
        db_table = 'profile_med'
        managed = False
        verbose_name = 'Профиль КИСа'
        verbose_name_plural = 'Профили КИСа'
        ordering = ['name']

    def __str__(self):
        return f'[КИС] ID: {self.id}, Профиль: {self.name}'

    def __repr__(self):
        return f'Profile(name=\'{self.name}\''
