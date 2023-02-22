import asyncio
import logging
import os
from typing import Callable

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, storage
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from config import load_config
from filters.admin import AdminFilter
from handlers import setup_handlers
from utils.notify_admins import notify_admins
from utils.set_bot_commands import set_default_commands


async def main():
    logging.basicConfig(filename='main.log', filemode='w', format='%(asctime)s | %(name)s - %(levelname)s - %(message)s')
    config = load_config()
    storage = MemoryStorage()
    engine: AsyncEngine = create_async_engine(
        f'postgresql+asyncpg://{config.db.username}:{config.db.password}@{config.db.host}/'
        f'{config.db.database}', echo=False, future=True)
    db_sessionmaker: Callable = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    bot = Bot(token=config.bot.token)
    dp = Dispatcher(bot, storage=storage)
    dp.filters_factory.bind(AdminFilter)

    setup_handlers(dp)
    await set_default_commands(dp)
    await notify_admins(dp, config.bot.admins)
    try:
        logging.warning('Bot started!')
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await (await bot.get_session()).close()
        await engine.dispose()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning('Bot stopped!')
