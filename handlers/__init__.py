from aiogram import Dispatcher
from handlers.main_handlers import register_main_handlers
from handlers.unknown_messages import register_unknown_messages_handlers


def setup_handlers(dp: Dispatcher):
    register_main_handlers(dp)
    register_unknown_messages_handlers(dp)