from typing import Never
from celery import shared_task
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .kis_data import DataForDMK, KISData, QuerySets


schedule, _ = CrontabSchedule.objects.get_or_create(
    minute='0',
    hour='7',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)

PeriodicTask.objects.get_or_create(
    crontab=schedule,
    name='Saving data to DMK',
    task='pg_processing.tasks.insert_data'
)


@shared_task
def insert_data() -> Never:
    """
    Update the MainData model with the collected data.

     Do this everyday at 7:00 AM by schedule.
    """
    ready_data = DataForDMK(KISData(QuerySets().queryset_for_dmk()))
    ready_data.save_to_dmk()


