from datetime import timedelta, datetime, time
from typing import List

from aiogram.dispatcher import FSMContext

from bot.keyboards.inline.task import get_todo_inline_markup, get_completed_inline_markup, get_edit_task_markup
from loader import _, dp
from aiogram.types import Message, CallbackQuery, callback_query

from models import User
from models.task import Task
from services.tasks import create_task, change_is_done, get_to_do, get_completed, get_task_by_id, delete_by_id
from services.users import get_user


async def _set_periodicity(periodicity):
    td = timedelta()
    parts = periodicity.split()
    for part in parts:
        if part[-1] == 'd':
            td += timedelta(days=int(part[:-1]))
        elif part[-1] == 'h':
            td += timedelta(hours=int(part[:-1]))
        elif part[-1] == 'm':
            td += timedelta(minutes=int(part[:-1]))
    return td


async def _is_input_earlier_today(input_date):
    return datetime.now().date() > input_date.date()


async def _is_input_time_earlier_now_time(input_date, input_time: time):
    if datetime.now().date() == input_date:
        return datetime.now().time() > input_time
    else:
        return False


async def _view_tasks(message: Message, tasks: List[Task], param: str):
    if not tasks:
        await message.answer(_(f'No {param} tasks.'))
        return
    else:
        await message.answer(_(f'Your {param} list:\n'))
        for task in tasks:
            await _view_task(message, task, param)


async def _view_task(message: Message, task: Task, param: str):
    response = f"{task.id}. {task.text} - {task.date} at {task.time}"
    if task.periodicity != 'no':
        response += f", {task.periodicity}\n"
    else:
        response += "\n"
    if param == 'to-do':
        await message.answer(response, reply_markup=get_todo_inline_markup())
    elif param == 'completed':
        await message.answer(response, reply_markup=get_completed_inline_markup())
    elif param == 'single':
        await message.answer(response, reply_markup=get_edit_task_markup())


async def _save_task(message: Message, state: FSMContext, user: User):
    data = await state.get_data()
    task_text = data['text']
    task_date = data['date']
    task_time = data['time']
    task_periodicity = data.get('periodicity', None)
    create_task(user.id, task_text, task_date, task_time, task_periodicity)
    await state.finish()
    await message.answer(_('Task added successfully.'))


async def to_do_done_callback(query: CallbackQuery, callback_data: dict, user: User):
    task_id = int(callback_data['task_id'])
    change_is_done(task_id)
    tasks = get_to_do(user.id)
    await _view_tasks(query.message, tasks, 'to-do')
    await callback_query.answer()


async def completed_done_callback(query: CallbackQuery, callback_data: dict, user: User):
    task_id = int(callback_data['task_id'])
    task = get_task_by_id(task_id)
    task.done_date = None
    change_is_done(task_id)
    tasks = get_completed(user.id)
    await _view_tasks(query.message, tasks, 'completed')
    await callback_query.answer()


async def delete_callback(query: CallbackQuery, callback_data: dict, user: User):
    task_id = int(callback_data['task_id'])
    delete_by_id(task_id)
    tasks = get_to_do(user.id)
    await _view_tasks(query.message, tasks, 'to-do')
    await callback_query.answer()