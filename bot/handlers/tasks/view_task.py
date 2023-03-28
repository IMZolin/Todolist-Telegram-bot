from typing import List
from aiogram.types import Message

from bot.keyboards.inline.task import get_delete_all_markup, get_todo_inline_markup, get_completed_inline_markup, \
    get_edit_task_markup
from models.task import Task
from loader import _
from aiogram.utils.markdown import bold, italic, text


async def _view_tasks(message: Message, tasks: List[Task], param: str):
    if not tasks:
        await message.answer(_(f'No {param} tasks.'))
        return
    else:
        if param == 'to-do':
            response = _(f'📃Your {param} list📃\n\n')
        elif param == 'completed':
            response = _(f'🏆Your {param} list🏆\n\n')
        for task in tasks:
            response = await _view_task(message, task, param, response)
        await message.answer(response, reply_markup=get_delete_all_markup(param), parse_mode='HTML')


async def _view_task(message: Message, task: Task, param: str, response: str):
    task_message = _(f"<b>{task.id}. {task.text}</b>\n<u>{task.date}</u> at <u>{task.time}</u>")
    if task.periodicity != 'no':
        task_message += _(f"\n<i>periodicity: {task.periodicity}\n\n</i>")
    else:
        task_message += "\n\n"
    response += task_message
    if param == 'to-do':
        return response
    elif param == 'to-do-choose':
        await message.answer(task_message, reply_markup=get_todo_inline_markup(task), parse_mode='HTML')
    elif param == 'completed':
        return response
    elif param == 'completed-choose':
        await message.answer(task_message, reply_markup=get_completed_inline_markup(task), parse_mode='HTML')
    elif param == 'edit':
        await message.answer(task_message, reply_markup=get_edit_task_markup(task), parse_mode='HTML')
    elif param == 'add':
        await message.answer(task_message, parse_mode='HTML')

