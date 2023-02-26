from aiogram.types import Message

from bot.keyboards.default import get_default_markup
from loader import dp, _
from models import User


# @dp.message_handler(content_types=['text'])
# async def _default_menu(message: Message, user: User):
#     await message.answer(_('Choose an action from the menu 👇'))
