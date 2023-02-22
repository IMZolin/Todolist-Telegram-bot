from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Start bot'),
        types.BotCommand('help', 'Help'),
        types.BotCommand('todolist', 'View the to-do list'),
        types.BotCommand('completedcases', 'View a list of completed cases'),
    ])