from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


def get_yes_no_inline_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(_('No'), callback_data='no'))
    markup.add(InlineKeyboardButton(_('Yes'), callback_data='yes'))

    return markup


def get_todo_inline_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(_('Done ✅'), callback_data='done'))
    markup.add(InlineKeyboardButton(_('Delete 🗑️'), callback_data='delete'))
    markup.add(InlineKeyboardButton(_('Edit ✏'), callback_data='edit'))
    markup.add(InlineKeyboardButton(_('Back 🔙'), callback_data='back'))
    return markup


def get_completed_inline_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(_('Not done ❌'), callback_data='done'))
    markup.add(InlineKeyboardButton(_('Back 🔙'), callback_data='back'))
    return markup