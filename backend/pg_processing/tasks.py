from backend.celery import app
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .kis_data import DataForDMK


schedule, _ = CrontabSchedule.objects.get_or_create(
    minute='*',
    hour='*',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)

PeriodicTask.objects.get_or_create(
    crontab=schedule,
    name='Saving data to DMK',
    task='pg_processing.tasks.update_data'
)


@app.task
def update_data():
    """
    Updates the MainData model with the collected data.

    :return: *None*
    """
    print('yes')

