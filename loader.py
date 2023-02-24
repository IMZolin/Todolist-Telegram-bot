from aiogram import Bot, Dispatcher
from peewee import PostgresqlDatabase

from bot.middlewares.i18n import i18n
from data.config import load_config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

config = load_config()
bot = Bot(token=config.bot.token)
if config.db.username and config.db.password and config.db.host and config.db.port and config.db.database:
    database = PostgresqlDatabase(config.db.database, user=config.db.username, password=config.db.password,
                                  host=config.db.host, port=config.db.port)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, run_tasks_by_default=True)
_ = i18n.gettext
