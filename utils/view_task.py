from typing import List, Optional

from aiogram import Bot
from aiogram.types import Message

from bot.keyboards.inline.task import get_delete_all_markup, get_todo_inline_markup, get_completed_inline_markup, \
    get_edit_task_markup
from data import config
from models.task import Task
from loader import _

config = config.load_config()


async def _view_tasks(tasks: List[Task], param: str, message: Optional[Message] = None, bot: Optional[Bot] = None):
    if not tasks and message:
        await message.answer(_(f'No {param} tasks.'))
        return
    else:
        response = ''
        if param == 'to-do':
            response = _(f'📃Your {param} list📃\n\n')
        elif param == 'completed':
            response = _(f'🏆Your {param} list🏆\n\n')
        for task in tasks:
            response = await _view_task(task, param, response, message, bot)
        if message:
            await message.answer(response, reply_markup=get_delete_all_markup(param), parse_mode='HTML')


async def _view_task(task: Task, param: str, response: str, message: Optional[Message] = None, bot: Optional[Bot] = None):
    task_message = _(f"<b>{task.id}. {task.text}</b>\n<u>{task.date}</u> at <u>{task.time}</u>")
    if task.periodicity != 'no':
        task_message += _(f"\n<i>periodicity: {task.periodicity}\n\n</i>")
    else:
        task_message += "\n\n"
    response += task_message
    if param == 'to-do':
        return response
    elif param == 'to-do-choose':
        await message.answer(response, reply_markup=get_todo_inline_markup(task), parse_mode='HTML')
    elif param == 'completed':
        return response
    elif param == 'completed-choose':
        await message.answer(response, reply_markup=get_completed_inline_markup(task), parse_mode='HTML')
    elif param == 'edit':
        await message.answer(response, reply_markup=get_edit_task_markup(task), parse_mode='HTML')
    elif param == 'add':
        await message.answer(response, parse_mode='HTML')
    elif param == 'notify':
        notify_text = _(f'❗NOTIFICATION❗\n\n' 
                        f'{task_message}\n<b>Deadline: {task.time}</b>')
        await bot.send_message(chat_id=task.author, text=notify_text,  reply_markup=get_todo_inline_markup(task), parse_mode='HTML')   
    await _view_files(task=task, bot=bot)


async def _view_files(task: Task, bot: Bot):
    attachments = list()
    files = list()
    if not task.attachments is None:
        attachments = task.attachments.split(';')
        attachments.pop(-1)
        for attachment in attachments:
            file_info = attachment.split(',')
            files.append({'id':file_info[0],
                        'type':file_info[1]})
        for file in files:
            if file['type'] == 'document':
                await bot.send_document(chat_id=task.author, document=file['id'])
                # media.attach_document(document=file['id'])
            if file['type'] == 'photo':
                await bot.send_photo(chat_id=task.author, photo=file['id'])
                # media.attach_photo(photo=file['id'])
            if file['type'] == 'video':
                await bot.send_video(chat_id=task.author, video=file['id'])
                # media.attach_video(video=file['id'])
            if file['type'] == 'audio':
                await bot.send_audio(chat_id=task.author, audio=file['id'])
