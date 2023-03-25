from aiogram.types import CallbackQuery

from bot.handlers.tasks.view_task import _view_tasks
from loader import dp, _
from models import User
from services.tasks import get_task_by_id, delete_all_tasks, delete_by_id, get_to_do, change_is_done


@dp.callback_query_handler(lambda c: c.data.startswith(('delete_all_to-do_tasks', 'delete_all_completed_tasks')))
async def delete_all_tasks_callback_handler(callback_query: CallbackQuery, user: User):
    param = callback_query.data.split('_')[2]
    delete_all_tasks(user.id, param)
    await callback_query.answer(_('All tasks have been deleted.'))
    await callback_query.message.edit_reply_markup(reply_markup=None)


@dp.callback_query_handler(lambda c: c.data.startswith('delete_task_'))
async def _choose_task_delete(callback_query: CallbackQuery, user: User):
    task_id = int(callback_query.data.split('_')[-1])
    task = get_task_by_id(task_id)
    delete_by_id(task_id)
    tasks = get_to_do(user.id)
    await callback_query.message.delete()
    await callback_query.message.answer(_(f'Your task {task.text} was deleted'))
    await _view_tasks(callback_query.message, tasks, 'to-do')


@dp.callback_query_handler(lambda c: c.data.startswith('is_done_'))
async def _choose_task_is_done(callback_query: CallbackQuery, user: User):
    task_id = int(callback_query.data.split('_')[-1])
    task = get_task_by_id(task_id)
    change_is_done(task_id)
    tasks = get_to_do(user.id)
    await callback_query.message.delete()
    await callback_query.message.answer(_(f'Your task {task.text} is done'))
    await _view_tasks(callback_query.message, tasks, 'to-do')
