from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram.types import Message

from bot.commands import get_default_commands
from bot.keyboards.inline import get_language_inline_markup
from loader import dp, _
from models import User


@dp.message_handler(i18n_text='View to-do list 📃')
@dp.message_handler()
async def _to_do_list(message: Message, user: User):
    commands = get_default_commands(user.language)

    text = _('Help 🆘') + '\n\n'
    for command in commands:
        text += f'{command.command} - {command.description}\n'

    await message.answer(text)


@dp.message_handler(i18n_text='View completed cases🏆')
@dp.message_handler()
async def _completed_cases(message: Message, user: User):
    commands = get_default_commands(user.language)

    text = _('Help 🆘') + '\n\n'
    for command in commands:
        text += f'{command.command} - {command.description}\n'

    await message.answer(text)