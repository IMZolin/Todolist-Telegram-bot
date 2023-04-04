from datetime import datetime

from aiogram.dispatcher import FSMContext

from bot.forms.forms import EditTaskStateGroup
from bot.handlers.tasks.calendar import _select_date
from utils.view_task import _view_task
from loader import dp, _
from aiogram.types import Message, CallbackQuery

from models import User
from services.tasks import get_task_by_id, update_task
from utils.task_helpers import _save_task, _set_periodicity, _body_set_date
from aiogram_calendar import simple_cal_callback


@dp.callback_query_handler(lambda c: c.data.startswith('edit_text_'), state=EditTaskStateGroup.inlineMenu)
async def _edit_text(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.delete()
    task_id = int(callback_query.data.split('_')[-1])
    await callback_query.message.answer(_('Enter new description of your task'))
    await EditTaskStateGroup.text.set()
    async with state.proxy() as data:
        data['task_id'] = task_id


@dp.message_handler(state=EditTaskStateGroup.text)
async def _edit_task_text(message: Message, state: FSMContext, user: User) -> None:
    task_id = (await state.get_data())['task_id']
    task_text = message.text
    await update_task(task_id, task_text)
    await _save_task(message, state, user, 'edit', task_id)
    await _view_task(get_task_by_id(task_id), 'edit', '', message)


@dp.callback_query_handler(lambda c: c.data.startswith('edit_date_'), state=EditTaskStateGroup.inlineMenu)
async def _edit_date(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.delete()
    task_id = int(callback_query.data.split('_')[-1])
    await _select_date(callback_query.message)
    await EditTaskStateGroup.date.set()
    async with state.proxy() as data:
        data['task_id'] = task_id


@dp.callback_query_handler(simple_cal_callback.filter(), state=EditTaskStateGroup.date)
async def _edit_task_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext, user: User) -> None:
    task_id = (await state.get_data())['task_id']
    selected, task_date = await _body_set_date(callback_query, callback_data, state)
    if selected:
        await update_task(task_id, None, task_date)
        await _save_task(callback_query.message, state, user, 'edit', task_id)
        await _view_task(get_task_by_id(task_id), 'edit', '', callback_query.message)


@dp.callback_query_handler(lambda c: c.data.startswith('edit_time_'), state=EditTaskStateGroup.inlineMenu)
async def _edit_time(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.delete()
    task_id = int(callback_query.data.split('_')[-1])
    await callback_query.message.answer(_('At what time should the task be done?\nPlease enter in format '
                                          f'H:M.'))
    await EditTaskStateGroup.time.set()
    async with state.proxy() as data:
        data['task_id'] = task_id


@dp.message_handler(state=EditTaskStateGroup.time)
async def _edit_task_time(message: Message, state: FSMContext, user: User) -> None:
    task_id = (await state.get_data())['task_id']
    task = get_task_by_id(task_id)
    try:
        task_time = datetime.strptime(message.text, '%H:%M')
        if datetime.now().date() == task.date and datetime.now().time() > task_time.time():
            await message.answer(_("Selected time is earlier than current time. Please select a later time."))
            return
        else:
            await update_task(task_id, None, None, task_time)
            await _save_task(message, state, user, 'edit', task_id)
            await _view_task(get_task_by_id(task_id), 'edit', '', message)
    except ValueError:
        await message.answer(_("Incorrect time format. Please enter in format hh:mm."))


@dp.callback_query_handler(lambda c: c.data.startswith('edit_periodicity_'), state=EditTaskStateGroup.inlineMenu)
async def _edit_periodicity(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.delete()
    task_id = int(callback_query.data.split('_')[-1])
    await callback_query.message.answer(_('Enter the frequency of your task in the format Xy Xm Xw Xd, where X is '
                                          'a number (for example, 1y 1m 1w 1d) or enter non-periodic task.'))
    await EditTaskStateGroup.periodicity.set()
    async with state.proxy() as data:
        data['task_id'] = task_id


@dp.message_handler(state=EditTaskStateGroup.periodicity)
async def _edit_task_text(message: Message, state: FSMContext, user: User) -> None:
    task_periodicity = message.text.strip()
    task_id = (await state.get_data())['task_id']
    if task_periodicity == 'no':
        await update_task(task_id, None, None, None, 'no')
        await _save_task(message, state, user, 'edit', task_id)
        await _view_task(get_task_by_id(task_id), 'edit', '', message)
    else:
        try:
            td = await _set_periodicity(task_periodicity)
        except:
            await message.answer(_('Invalid periodicity format. Please enter the correct format (for '
                                   'example, 1y 1m 1w 1d) or enter "no" for a non-periodic task.'))
            return
        await update_task(task_id, None, None, None, td)
        await _save_task(message, state, user, 'edit', task_id)
        await _view_task(get_task_by_id(task_id), 'edit', '', message)