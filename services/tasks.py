import calendar
from datetime import datetime, timedelta
from typing import List, Optional
from utils.misc.logging import logger
from models import User
from models.task import Task
from loader import _
from dateutil.relativedelta import relativedelta
from peewee import DoesNotExist


def get_tasks(user_id: int) -> List[Task]:
    return Task.select().where(Task.author == user_id)


def get_to_do(user_id: int) -> List[Task]:
    tasks = get_tasks(user_id)
    return [task for task in tasks if not task.is_done]


def get_completed(user_id: int) -> List[Task]:
    tasks = get_tasks(user_id)
    return [task for task in tasks if task.is_done]


def create_task(user_id: int, task_name: str, task_date: datetime, task_time: datetime, periodicity: str, attachments: str):
    user = User.get(User.id == user_id)
    new_task = Task.create(author=user, text=task_name, date=task_date, time=task_time, periodicity=periodicity, attachments=attachments)
    new_task.save()
    return new_task.id


def get_task_by_id(id: int) -> Optional[Task]:
    task = Task.get_or_none(Task.id == id)
    if task is None:
        logger.exception(f'No task found with id {id}')
        # raise ValueError(_(f"No task found with id {id}"))
    
    return task


def get_task_by_date(time: str) -> List[Task]:
    return Task.select().where((Task.time == time) & (Task.is_done == False))


def change_is_done(id: int) -> None:
    task = get_task_by_id(id)
    is_done = task.is_done
    if task.periodicity == 'no':
        task.is_done = not is_done
    else:
        try:
            # parse the number of days from the periodicity string
            days = int(task.periodicity.split()[0])

            # add the remaining days to the end of the month
            remaining_days = calendar.monthrange(task.date.year, task.date.month)[1] - task.date.day
            if remaining_days < days:
                task.date += timedelta(days=remaining_days)
                days -= remaining_days
            else:
                task.date += timedelta(days=days)
                days = 0

            # add the remaining days to the end of each month
            while days > 0:
                # calculate the number of days in the next month
                next_month = task.date.replace(day=1) + relativedelta(months=1)
                days_in_month = (next_month - timedelta(days=1)).day

                # add the remaining days to the end of the month
                if days_in_month <= days:
                    task.date = next_month
                    days -= days_in_month
                else:
                    task.date = next_month.replace(day=days)
                    days = 0
        except ValueError as e:
            logger.exception(f"Invalid periodicity format: {task.periodicity}")
            return
    task.done_date = datetime.now() if task.is_done else None
    task.save()


def add_days_to_date(date: datetime, days: int) -> datetime:
    days_in_month = (date.replace(day=1) + timedelta(days=32)).day - 1
    days_left = days_in_month - date.day + 1
    if days <= days_left:
        return date + timedelta(days=days)
    else:
        next_month = date.replace(day=1) + timedelta(days=32)
        days_to_add = days - days_left
        return next_month.replace(day=1) + timedelta(days=days_to_add - 1)


def delete_by_id(id: int) -> None:
    task = get_task_by_id(id)
    task.delete_instance()


async def update_task(id: int, text: Optional[str] = None, date: Optional[datetime] = None,
                      time: Optional[datetime] = None, periodicity: Optional[str] = None) -> bool:
    task = get_task_by_id(id)
    if task is None:
        return False
    if text is not None:
        task.text = text
    if date is not None:
        task.date = date.date()
    if time is not None:
        task.time = time.time()
    if periodicity is not None:
        task.periodicity = periodicity
    task.save()
    return True


def delete_all_tasks(user_id: int, param: str) -> None:
    tasks = Task.select().where(Task.author == user_id)
    if param == 'to-do':
        tasks_del = tasks.where(Task.is_done == False)
    elif param == 'completed':
        tasks_del = tasks.where(Task.is_done == True)
    else:
        logger.exception(f'Invalid parameter.')
        return
    deleted_count = 0
    for task in tasks_del:
        task.delete_instance()
        deleted_count += 1
    if deleted_count == 0:
        logger.exception(f'No tasks to delete.')
    else:
        logger.exception(f'{deleted_count} tasks have been deleted.')


def add_attachment_by_id(task_id: int, attachment: str):
    task = Task.get_or_none(Task.id == task_id)
    if task is None:
        logger.exception(f"No Task found with id {task_id}")
    
    new_attachments = task.attachments + ";" + attachment
    task.attachments = new_attachments
    task.save()


def delete_attachments_by_id(task_id: int, indices: List[int]) -> int:
    try:
        task = Task.get_by_id(task_id)
    except DoesNotExist:
        return -1
    
    attachments = task.attachments.split(';')
    attachments.pop(-1)
    
    for index in indices:
        if index < 0 or index >= len(attachments):
            return -1
    
    new_attachments = [att for idx, att in enumerate(attachments) if idx not in indices]
    new_attachments_str = ';'.join(new_attachments) + ';'
    
    task.attachments = new_attachments_str
    task.save()
    
    return 0