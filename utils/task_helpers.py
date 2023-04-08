from datetime import timedelta, datetime, time
from typing import Optional

from aiogram.dispatcher import FSMContext
from aiogram_calendar import SimpleCalendar

from bot.forms.forms import EditTaskStateGroup
from bot.handlers.tasks.calendar import _process_simple_calendar
from loader import _
from aiogram.types import Message, CallbackQuery

from models import User
from models.task import Task
from services.tasks import create_task, get_task_by_id
import re


async def _set_periodicity(periodicity):
    td = timedelta()
    parts = re.findall(r'(\d+)\s*(\w)', periodicity)
    for value, unit in parts:
        value = int(value)
        if unit == 'w':
            td += timedelta(weeks=value)
        elif unit == 'd':
            td += timedelta(days=value)
        elif unit == 'm':
            td += timedelta(days=value*30)
        elif unit == 'y':
            td += timedelta(days=value*365)

    if td == timedelta():  # Input was not correctly processed
        raise ValueError('Invalid periodicity format. Please enter the correct format (for example, 1y or(and) 1m or(and) 1w or(and) 1d) or enter no for a non-periodic task.')
    return td


async def _is_input_earlier_today(input_date):
    return datetime.now().date() > input_date.date()


async def _is_input_time_earlier_now_time(input_date, input_time: time):
    return datetime.now().date() == input_date and datetime.now().time() > input_time


async def _save_task(message: Message, state: FSMContext, user: User, param: str, task_id: Optional[int] = None) -> Task:
    data = await state.get_data()
    if param == "add":
        task_text = data['text']
        task_date = data['date']
        task_time = data['time']
        task_periodicity = data.get('periodicity', None)
        task_attachments = data['attachments']
        created_id = create_task(user.id, task_text, task_date, task_time, task_periodicity, task_attachments)
        task = get_task_by_id(created_id)
        await state.finish()
    else:
        task = get_task_by_id(task_id)
        await EditTaskStateGroup.inlineMenu.set()
    if param == "add":
        await message.answer(_('Task added successfully.'))
    else:
        await message.answer(_('Task edited successfully.'))
    return task


async def _body_set_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await _process_simple_calendar(callback_query, callback_data)

    async with state.proxy() as data:
        data['date'] = date.strftime("%d.%m.%Y")

    while selected and await _is_input_earlier_today(date):
        await callback_query.message.answer(_("Wrong date. Please enter the day before today"),
                                            reply_markup=await SimpleCalendar().start_calendar())
        selected, date = await _process_simple_calendar(callback_query, callback_data)
    return selected, date

