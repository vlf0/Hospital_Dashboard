"""Here is described schedule and tasks for executing it using CELERY."""
from celery import shared_task
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .kis_data import DataForDMK, KISData, QuerySets
from .models import AccumulationOfIncoming
from .caching import Cacher


# Schedule for main logic - inserting data to DMK
schedule1, _ = CrontabSchedule.objects.get_or_create(
    minute='25',
    hour='11',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)

# Schedule for acuumulativing logic - inserting data to DMK
schedule2, _ = CrontabSchedule.objects.get_or_create(
    minute='0',
    hour='6',
    day_of_week='*',
    day_of_month='1',
    month_of_year='*',
)


@shared_task
def cache_all_data():
    """
    Remove all day caches, process and insert data into DMK.

     Update the MainData model with the collected data.
     Do this everyday at 7:00 AM by schedule.
    """
    ready_data = DataForDMK(KISData(QuerySets().queryset_for_dmk()))
    ready_data.save_to_dmk()
    Cacher().main_caching()


@shared_task
def remove_accum():
    AccumulationOfIncoming.objects.truncate_data()


tasks_settings = {
    'cache_task': ('Saving data to DMK', cache_all_data.name, schedule1),
    'remove_task': ('Removing accumulated data from DMK', remove_accum.name, schedule2),
}


def get_or_create_tasks(tasks_list):
    for options in tasks_list.values():
        name = options[0]
        task = options[1]
        schedule = options[2]
        try:
            task = PeriodicTask.objects.get(name=name)
            if task.crontab_id != schedule.id:
                task.crontab_id = schedule.id
                task.save()
            continue
        except:
            PeriodicTask.objects.create(crontab=schedule,
                                        name=name,
                                        task=task,
                                        )


get_or_create_tasks(tasks_settings)
