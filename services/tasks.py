import calendar
from datetime import datetime, timedelta
from typing import List, Optional

from models import User
from models.task import Task
from loader import _
from dateutil.relativedelta import relativedelta


def get_tasks(user_id: int) -> List[Task]:
    return Task.select().where(Task.author == user_id)


def get_to_do(user_id: int) -> List[Task]:
    tasks = get_tasks(user_id)
    return [task for task in tasks if not task.is_done]


def get_completed(user_id: int) -> List[Task]:
    tasks = get_tasks(user_id)
    return [task for task in tasks if task.is_done]


def create_task(user_id: int, task_name: str, task_date: datetime, task_time: datetime, periodicity: str):
    user = User.get(User.id == user_id)
    new_task = Task.create(author=user, text=task_name, date=task_date, time=task_time, periodicity=periodicity)
    new_task.save()
    return new_task.id


def get_task_by_id(id: int) -> Optional[Task]:
    task = Task.get_or_none(Task.id == id)
    if task is None:
        raise ValueError(_(f"No task found with id {id}"))
    return task


def get_task_by_date(user_id: int, time: str) -> List[Task]:
    tasks = get_tasks(user_id)
    return [task for task in tasks if not task.is_done and task.date == datetime.now().date() and task.time == time]


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
            print(_(f"Invalid periodicity format: {task.periodicity}"))
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
    # from utils.task_helpers import _set_periodicity
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
        # td = await _set_periodicity(periodicity)
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
        print(_('Invalid parameter.'))
        return
    deleted_count = 0
    for task in tasks_del:
        task.delete_instance()
        deleted_count += 1
    if deleted_count == 0:
        print(_('No tasks to delete.'))
    else:
        print(f'{deleted_count} tasks have been deleted.')
