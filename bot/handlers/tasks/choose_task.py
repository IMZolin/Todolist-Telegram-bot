from typing import List

from aiogram.types import Message, CallbackQuery

from bot.forms.forms import EditTaskStateGroup
from utils.view_task import _view_task
from bot.keyboards.inline.task import get_ids_to_do, get_ids_completed, get_ids_edit
from loader import _, dp, bot
from models.task import Task
from services.tasks import get_task_by_id


async def _choose_task(message: Message, tasks: List[Task], param: str):
    text = _('Choose id of task')
    if param == 'to-do':
        await message.answer(text, reply_markup=get_ids_to_do(tasks))
    elif param == 'completed':
        await message.answer(text, reply_markup=get_ids_completed(tasks))
    elif param == 'edit':
        await message.answer(text, reply_markup=get_ids_edit(tasks))


@dp.callback_query_handler(lambda c: c.data.startswith('task_to_do_'))
async def _choose_task_to_do(callback_query: CallbackQuery):
    task_id = int(callback_query.data.split('_')[-1])
    task = get_task_by_id(task_id)
    response = ''
    await callback_query.message.delete()
    await _view_task(task, 'to-do-choose', response, callback_query.message, bot)


@dp.callback_query_handler(lambda c: c.data.startswith('task_completed_'))
async def _choose_task_completed(callback_query: CallbackQuery):
    task_id = int(callback_query.data.split('_')[-1])
    task = get_task_by_id(task_id)
    response = ''
    await callback_query.message.delete()
    await _view_task(task, 'completed-choose', response, callback_query.message, bot)


@dp.callback_query_handler(lambda c: c.data.startswith('task_edit_'))
async def _choose_task_edit(callback_query: CallbackQuery):
    task_id = int(callback_query.data.split('_')[-1])
    task = get_task_by_id(task_id)
    response = ''
    await callback_query.message.delete()
    await _view_task(task, 'edit', response, callback_query.message, bot)
    await EditTaskStateGroup.inlineMenu.set()
