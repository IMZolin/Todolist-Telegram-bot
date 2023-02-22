from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_kb_menu(name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(InlineKeyboardButton(f'{name}', callback_data='button_menu'))