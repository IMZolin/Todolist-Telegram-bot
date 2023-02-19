import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_to_do = types.KeyboardButton(text="View the to-do list")
    keyboard.add(button_to_do)
    button_completed = types.KeyboardButton(text="View a list of completed cases")
    keyboard.add(button_completed)
    await bot.send_message(message.from_user.id,
                           "Welcome!\nI can help you create and manage your tasks with a calendar and a reminder!",
                           reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.reply(
        "I can help you create and manage your tasks with a calendar and a reminder!\\ You can control me by sending "
        "these commands:\\some command")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
