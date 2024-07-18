"""This module defines the schedule and tasks for executing periodic tasks using Celery."""
from aiohttp import ClientSession, ClientError
import asyncio
from celery import shared_task, chain
from celery.result import AsyncResult
from django_celery_beat.models import PeriodicTask, CrontabSchedule, MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from data.kis_data import DataForDMK, KISData, MainQueries
from data.models import AccumulationOfIncoming
from data.caching import Cacher
from data.kis_data import today
from django.conf import settings

TG_TOKEN_DMK = settings.TG_TOKEN_DMK


async def bot_send_message(message: str) -> None:
    """
    Sends a message to the specified Telegram chat IDs.

    :param message: The message to send.
    """
    chat_ids = [406086387, 678666905, 893047326]
    url = f'https://api.telegram.org/bot{TG_TOKEN_DMK}/sendMessage'
    my_payload = {'chat_id': 0, 'text': message}
    async with ClientSession() as session:
        for chat_id in chat_ids:
            my_payload.update({'chat_id': chat_id})
            try:
                async with session.post(url, data=my_payload) as response:
                    response.raise_for_status()
            except ClientError as e:
                print(f'Error: {e}')


@shared_task
def send_notification(task_id: str) -> None:
    """
    Sends a notification about the status of a task.

    :param task_id: The ID of the task to check the status of.
    """
    task_result_id = AsyncResult(task_id)
    while not task_result_id.ready():
        pass
    task_result_status = task_result_id.status
    status_messages = {
        'SUCCESS': f'Date: {today()}\nTask was performed with status: [SUCCESS]',
        'FAILURE': f'Date: {today()}\nThe task was exited with error. '
                   f'You need to check the Celery logs. Task status: [FAILURE]'
    }
    message = status_messages.get(task_result_status, '')
    asyncio.run(bot_send_message(message))


@shared_task(bind=True)
def cache_all_data(self) -> str:
    """
    Caches data and saves it to DMK.

    This task processes the needed data and inserts them into DMK.
    It updates the MainData model with the collected data and runs daily at 6:00 AM by schedule.

    :return: The ID of the current task request.
    """
    ready_data = DataForDMK(KISData(MainQueries().create_dmk_query()))
    ready_data.save_to_dmk()
    Cacher().main_caching()
    return self.request.id


@shared_task
def chain_tasks() -> None:
    """
    Chains tasks to execute them sequentially.

    This task chains the `cache_all_data` task and the `send_notification` task.
    """
    chain(cache_all_data.s() | send_notification.s())()


@shared_task
def remove_accum() -> None:
    """
    Removes accumulated data from the DMK.

    This task truncates the data in the AccumulationOfIncoming model.
    """
    AccumulationOfIncoming.objects.truncate_data()


tasks = {
    1: ['Notification Chain Task', chain_tasks.name],
    2: ['Removing accumulated data from DMK', remove_accum.name],
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
    """Manages the scheduling and creation of periodic tasks."""

    def __init__(self):
        self.tasks_list = tasks
        self.schedules_list = schedules

    def check_schedules(self):
        """
        Checks and creates the necessary schedules in the CrontabSchedule model.
        """
        try:
            for schedule in self.schedules_list.items():
                CrontabSchedule.objects.get_or_create(**schedule[1])
        except MultipleObjectsReturned:
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE django_celery_beat_crontabschedule RESTART IDENTITY CASCADE;")
            self.check_schedules()

    def get_or_create_tasks(self):
        """
        Checks and creates the necessary periodic tasks in the PeriodicTask model if not exists.
        """
        self.check_schedules()
        tasks_ids = list(tasks)
        tasks_names = [tasks[task_id][0] for task_id in tasks_ids]
        PeriodicTask.objects.exclude(id__in=tasks_ids, name__in=tasks_names).delete()
        for crontab_id, options in self.tasks_list.items():
            name = options[0]
            task = options[1]
            schedule = CrontabSchedule.objects.get(pk=crontab_id)
            try:
                task = PeriodicTask.objects.get(pk=crontab_id, name=name)
                if task.crontab_id != schedule.id:
                    task.crontab_id = schedule.id
                    task.save()
            except ObjectDoesNotExist:
                PeriodicTask.objects.create(pk=crontab_id,
                                            crontab=schedule,
                                            name=name,
                                            task=task)


TasksManager().get_or_create_tasks()
