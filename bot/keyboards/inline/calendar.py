from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_calendar_inline_markup():
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(text='Simple calendar 🔢', callback_data='simple_calendar'))
    markup.add(InlineKeyboardButton(text='Dialog calendar 📅', callback_data='dialog_calendar'))

    return markup
