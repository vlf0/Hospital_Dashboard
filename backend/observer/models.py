from django.db import models
from dashboard.models import Profiles


class Departments(models.Model):

    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE, verbose_name='Профиль')
    name = models.CharField(max_length=255, verbose_name='Название отделения')
    active = models.BooleanField(default=True, verbose_name='Статус')

    class Meta:
        verbose_name = 'Отделение'
        verbose_name_plural = 'Отделения'
        ordering = ['name']

    def __str__(self):
        return f'[КИС] Профиль: {self.profile.name}, Отделение: {self.name}, Активен: {"Да" if self.active else "Нет"}'

    def __repr__(self):
        return (f'Departments(id=\'{self.id}\', profile_id=\'{self.profile.id}\','
                f' name=\'{self.name}\', active={self.active})')
