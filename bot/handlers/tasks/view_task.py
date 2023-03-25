from typing import List
from aiogram.types import Message

from bot.keyboards.inline.task import get_delete_all_markup, get_todo_inline_markup, get_completed_inline_markup, \
    get_edit_task_markup
from models.task import Task
from loader import _


async def _view_tasks(message: Message, tasks: List[Task], param: str):
    if not tasks:
        await message.answer(_(f'No {param} tasks.'))
        return
    else:
        response = _(f"📌Your {param} list\n\n")
        for task in tasks:
            response = await _view_task(message, task, param, response)
        await message.answer(response, reply_markup=get_delete_all_markup(param))


async def _view_task(message: Message, task: Task, param: str, response: str):
    task_message = f"{task.id}. {task.text}\n{task.date} at {task.time}"
    if task.periodicity != 'no':
        task_message += f"\nperiodicity: {task.periodicity}\n"
    else:
        task_message += "\n"
    response += task_message
    if param == 'to-do':
        return response
    elif param == 'to-do-choose':
        await message.answer(task_message, reply_markup=get_todo_inline_markup(task))
    elif param == 'completed':
        return response
    elif param == 'completed-choose':
        await message.answer(task_message, reply_markup=get_completed_inline_markup(task))
    elif param == 'edit':
        await message.answer(task_message, reply_markup=get_edit_task_markup(task))
    elif param == 'add':
        await message.answer(task_message)

