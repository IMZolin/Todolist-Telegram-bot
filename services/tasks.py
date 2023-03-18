from datetime import datetime
from typing import List, Optional

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


def get_task_by_id(id: int) -> Optional[Task]:
    task = Task.get_or_none(Task.id == id)
    if task is None:
        raise ValueError(f"No task found with id {id}")
    return task


def change_is_done(id: int) -> None:
        task = get_task_by_id(id)
        is_done = task.is_done
        task.is_done = not is_done
        task.done_date = datetime.now() if task.is_done else None
        task.save()


def delete_by_id(id: int) -> None:
    task = get_task_by_id(id)
    task.delete_instance()


async def update_task(id: int, text: Optional[str] = None, date: Optional[datetime] = None, time: Optional[datetime] = None, periodicity: Optional[str] = None) -> bool:
    from utils.task_helpers import _set_periodicity
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
        td = await _set_periodicity(periodicity)
        task.periodicity = td
    task.save()
    return True




