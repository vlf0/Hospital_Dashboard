from typing import Never
from celery import shared_task
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .kis_data import DataForDMK, KISData, QuerySets


# Schedule for main logic - inserting data to DMK
schedule1, _ = CrontabSchedule.objects.get_or_create(
    minute='0',
    hour='7',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)

PeriodicTask.objects.get_or_create(
    crontab=schedule1,
    name='Saving data to DMK',
    task='pg_processing.tasks.insert_data'
)

# Schedule for removing all cache everyday
schedule2, _ = CrontabSchedule.objects.get_or_create(
    minute='59',
    hour='6',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)

PeriodicTask.objects.get_or_create(
    crontab=schedule2,
    name='Deleting day cache',
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


