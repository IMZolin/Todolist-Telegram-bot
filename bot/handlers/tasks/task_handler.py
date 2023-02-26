from aiogram.types import Message

from loader import dp, _
from models import User
from services.users import count_users


@dp.message_handler(i18n_text='Add a new task 🆕')
@dp.message_handler(commands=['new_task'])
async def _new_task(message: Message, user: User):
    await message.answer(_('Your new task'))


@dp.message_handler(i18n_text='View to-do list 📃')
@dp.message_handler(commands=['todo'])
async def _to_do_list(message: Message, user: User):
    await message.answer(_('Your to-do list'))


@dp.message_handler(i18n_text='View a list of completed cases 🏆')
@dp.message_handler(commands=['completed'])
async def _completed_cases(message: Message, user: User):
    count = count_users()

    await message.answer(_('Your list of completed cases'))


