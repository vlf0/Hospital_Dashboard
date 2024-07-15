"""Here is described schedule and tasks for executing it using CELERY."""
from celery import shared_task
from django_celery_beat.models import PeriodicTask, CrontabSchedule, MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from .kis_data import DataForDMK, KISData, MainQueries
from .models import AccumulationOfIncoming
from .caching import Cacher


@shared_task
def cache_all_data():
    """
    Remove all day caches, process and insert data into DMK.

     Update the MainData model with the collected data.
     Do this everyday at 6:00 AM by schedule.
    """
    ready_data = DataForDMK(KISData(MainQueries().create_dmk_query()))
    ready_data.save_to_dmk()
    Cacher().main_caching()


@shared_task
def remove_accum():
    AccumulationOfIncoming.objects.truncate_data()


tasks = {
    '1': ['Saving data to DMK', cache_all_data.name],
    '2': ['Removing accumulated data from DMK', remove_accum.name],
}

schedules = {
    '1': {
        'minute': '0',
        'hour': '6',
        'day_of_week': '*',
        'day_of_month': '*',
        'month_of_year': '*',
    },
    '2': {
        'minute': '59',
        'hour': '5',
        'day_of_week': '*',
        'day_of_month': '1',
        'month_of_year': '*',
    }
}


class TasksManager:

    def __init__(self):
        self.tasks_list = tasks
        self.schedules_list = schedules

    def check_schedules(self):
        try:
            for schedule in self.schedules_list.items():
                CrontabSchedule.objects.get_or_create(**schedule[1])
        except MultipleObjectsReturned:
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE django_celery_beat_crontabschedule RESTART IDENTITY CASCADE;")
            self.check_schedules()

    def get_or_create_tasks(self):
        self.check_schedules()
        for crontab_id, options in self.tasks_list.items():
            name = options[0]
            task = options[1]
            schedule = CrontabSchedule.objects.get(pk=crontab_id)
            try:
                task = PeriodicTask.objects.get(name=name)
                if task.crontab_id != schedule.id:
                    task.crontab_id = schedule.id
                    task.save()
                continue
            except ObjectDoesNotExist:
                PeriodicTask.objects.create(crontab=schedule,
                                            name=name,
                                            task=task,
                                            )


TasksManager().get_or_create_tasks()
