from aiogram import types, Dispatcher
from aiogram.types import ChatType

from database.dao.holder import DAO
from keyboard.inline import get_kb_menu


async def cmd_start(message: types.Message):
    # user = await dao.user.create(message.chat.id, message.chat.username)
    await message.answer(f'Welcome, @{message.chat.username if message.chat.username else "human"}!\nI can help you create and manage your tasks with a calendar and a reminder!\n')


async def cmd_help(message: types.Message):
    await message.answer(
        "I can help you create and manage your tasks with a calendar and a reminder!\n You can control me by sending "
        "these commands:\n/todolist - View the to-do list\n/completedcases', 'View a list of completed cases")


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'], chat_type=ChatType.PRIVATE)
    dp.register_message_handler(cmd_help, commands=['help'], chat_type=ChatType.PRIVATE)