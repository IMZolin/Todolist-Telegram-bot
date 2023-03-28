from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _
from models import Task


def get_cancel_inline_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(_('Cancel'), callback_data='cancel'))
    return markup


def get_yes_no_inline_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(_('No'), callback_data='no'))
    markup.add(InlineKeyboardButton(_('Yes'), callback_data='yes'))
    return markup


def get_upload_files_inline_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(_('Add more files'), callback_data='add_more_files'))
    markup.add(InlineKeyboardButton(_('Finish adding files'), callback_data='finish_add_files'))
    return markup


def get_todo_inline_markup(task: Task):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(_('Done ✅'), callback_data=f'is_done_task_{task.id}'))
    markup.add(InlineKeyboardButton(_('Delete 🗑️'), callback_data=f'delete_task_{task.id}'))
    markup.add(InlineKeyboardButton(_('Edit ✏'), callback_data=f'task_edit_{task.id}'))
    markup.add(InlineKeyboardButton(_('Main menu 🔙'), callback_data='main_menu'))
    return markup


def get_completed_inline_markup(task: Task):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(_('Not done ❌'), callback_data=f'is_done_{task.id}'))
    markup.add(InlineKeyboardButton(_('Delete 🗑️'), callback_data=f'delete_task_{task.id}'))
    markup.add(InlineKeyboardButton(_('Main menu 🔙'), callback_data='main_menu'))
    return markup


def get_edit_task_markup(task: Task):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(_('Text 📄'), callback_data=f'edit_text_{task.id}'))
    markup.add(InlineKeyboardButton(_('Date 📅'), callback_data=f'edit_date_{task.id}'))
    markup.add(InlineKeyboardButton(_('Time ⌚'), callback_data=f'edit_time_{task.id}'))
    markup.add(InlineKeyboardButton(_('Periodicity 🔄️'), callback_data=f'edit_periodicity_{task.id}'))
    markup.add(InlineKeyboardButton(_('Main menu 🔙'), callback_data='main_menu'))
    return markup


def get_delete_all_markup(param: str):
    markup = InlineKeyboardMarkup()
    if param == 'to-do':
        data = 'delete_all_to-do_tasks'
    else:
        data = 'delete_all_completed_tasks'
    markup.add(InlineKeyboardButton(_('Delete all tasks 🗑️'), callback_data=data))
    markup.add(InlineKeyboardButton(_('Main menu 🔙'), callback_data='main_menu'))
    return markup


def _get_rows_task(param: str, tasks: List[Task]):
    buttons = [InlineKeyboardButton(task.id, callback_data=f"{param}{task.id}") for task in tasks]
    rows = [buttons[i:i + 5] for i in range(0, len(buttons), 5)]
    markup = InlineKeyboardMarkup(row_width=5)
    for row in rows:
        markup.add(*row)
    return markup


def get_ids_to_do(tasks: List[Task]):
    return _get_rows_task('task_to_do_', tasks)


def get_ids_edit(tasks: List[Task]):
    return _get_rows_task('task_edit_', tasks)


def get_ids_completed(tasks: List[Task]):
    return _get_rows_task('task_completed_', tasks)