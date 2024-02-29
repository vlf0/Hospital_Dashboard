"""Here is described schedule and tasks for executing it using CELERY."""
from celery import shared_task
from django.core.cache import cache
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .kis_data import DataForDMK, KISData, QuerySets
from .models import AccumulationOfIncoming


# Schedule for main logic - inserting data to DMK
schedule1, _ = CrontabSchedule.objects.get_or_create(
    minute='0',
    hour='7',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)

# Schedule for acuumulativing logic - inserting data to DMK
schedule2, _ = CrontabSchedule.objects.get_or_create(
    minute='0',
    hour='7',
    day_of_week='*',
    day_of_month='1',
    month_of_year='*',
)

PeriodicTask.objects.get_or_create(
    crontab=schedule1,
    name='Saving data to DMK',
    task='data.tasks.insert_data'
)

PeriodicTask.objects.get_or_create(
    crontab=schedule2,
    name='Removing accumulated data from DMK',
    task='data.tasks.remove_accum'
)


@shared_task
def insert_data():
    """
    Remove all day caches, process and insert data into DMK.

     Update the MainData model with the collected data.
     Do this everyday at 7:00 AM by schedule.
    """
    cache.delete_many(['dmk', 'kis'])
    ready_data = DataForDMK(KISData(QuerySets().queryset_for_dmk()))
    ready_data.save_to_dmk()


@shared_task
def remove_accum():

    AccumulationOfIncoming.objects.raw("""TRUNCATE public.data_accumulationofincoming;""")


