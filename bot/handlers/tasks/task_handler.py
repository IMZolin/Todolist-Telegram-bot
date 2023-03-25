from aiogram.types import Message

from bot.forms.forms import TaskStateGroup
from bot.handlers.tasks.choose_task import _choose_task
from bot.handlers.tasks.view_task import _view_tasks
from loader import dp, _
from models import User
from services.tasks import get_to_do, get_completed


@dp.message_handler(i18n_text='New task 🆕')
@dp.message_handler(commands=['new_task'])
async def new_task(message: Message) -> None:
    await TaskStateGroup.text.set()
    await message.answer(_('Your new task:\nEnter description of your task'))


@dp.message_handler(i18n_text='Edit task ✏')
@dp.message_handler(commands=['edit_task'])
async def edit_task(message: Message, user: User):
    tasks = get_to_do(user.id)
    await _view_tasks(message, tasks, 'to-do')
    if tasks:
        await _choose_task(message, tasks, 'edit')


@dp.message_handler(i18n_text='To-do list 📃')
@dp.message_handler(commands=['todo'])
async def to_do_list(message: Message, user: User):
    tasks = get_to_do(user.id)
    await _view_tasks(message, tasks, 'to-do')
    if tasks:
        await _choose_task(message, tasks, 'to-do')


@dp.message_handler(i18n_text='Completed cases 🏆')
@dp.message_handler(commands=['completed'])
async def completed_cases(message: Message, user: User):
    tasks = get_completed(user.id)
    await _view_tasks(message, tasks, 'completed')
    if tasks:
        await _choose_task(message, tasks, 'completed')


