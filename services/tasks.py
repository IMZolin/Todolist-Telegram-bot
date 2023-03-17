from datetime import datetime
from typing import List

from models import User
from models.task import Task


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


def get_task_by_id(id: int) -> Task:
    return Task.get_or_none(Task.id == id)



