"""Responsible for models (tables in DMK BD)."""
from django.db import models
from django.contrib import admin
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


class Profiles(models.Model):

    name = models.CharField(max_length=50, verbose_name='Название профиля')
    active = models.BooleanField(default=True, verbose_name='Статус')

    def __str__(self):
        return f'ID: {self.id}, Профиль: {self.name}, Активен: {"Да" if self.active else "Нет"}'

    def __repr__(self):
        return f'Profile(name=\'{self.name}\', active={self.active})'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['name']


class AccumulationOfIncoming(models.Model):
    """
    Represent table contains data of incoming patients sorted by depts.

    Accumulates data every day and gives them by request.
    """
    objects = CustomManager()

    dates = models.DateField(auto_now_add=True)
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    number = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['number'])
        ]


class PlanNumbers(models.Model):
    """Represent table containing plan numbers of each depts."""
    objects = CustomManager()

    profile = models.OneToOneField(Profiles, on_delete=models.CASCADE, verbose_name='Профиль', primary_key=True)
    plan = models.IntegerField(verbose_name='План')

    class Meta:
        indexes = [
            models.Index(fields=['plan'])
        ]
        verbose_name = 'План'
        verbose_name_plural = 'Планы профилей'
        ordering = ['profile']

    def __str__(self):
        return f'Profile_id: {self.profile.id}, Профиль: {self.profile.name}, Текущий план: {self.plan}'


