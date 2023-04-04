import asyncio

from aiogram import Dispatcher
from aiogram import executor
from aiogram.types import Update

from bot.commands import set_default_commands
from loader import dp, bot
from data.config import ADMINS
from utils.misc.logging import logger
from notifier import scheduler


async def on_startup(dispatcher: Dispatcher):
    logger.info('Bot startup')
    for admin_id in ADMINS:
        await bot.send_message(admin_id, 'bot started')
    await set_default_commands()
    asyncio.create_task(scheduler())


async def on_shutdown(dispatcher: Dispatcher):
    logger.warning('Shutting down..')

    await dp.storage.close()
    await dp.storage.wait_closed()

    logger.warning('Bye!')


if __name__ == '__main__':
    from bot.middlewares import setup_middleware
    from bot import filters, handlers

    setup_middleware(dp)

    executor.start_polling(dp, on_startup=on_startup)
