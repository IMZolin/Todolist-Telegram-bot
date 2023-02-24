from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from loader import _


def get_default_markup(user):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    markup.add(_('Help 🆘'), _('Settings 🛠'))

    if len(markup.keyboard) < 1:
        return ReplyKeyboardRemove()

    return markup