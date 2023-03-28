from datetime import datetime

from aiogram.dispatcher import FSMContext

from bot.forms.forms import TaskStateGroup
from bot.handlers.tasks.calendar import _select_date
from bot.handlers.tasks.view_task import _view_task
from bot.keyboards.inline.task import get_yes_no_inline_markup, get_upload_files_inline_markup
from loader import dp, _
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import simple_cal_callback

from models import User
from utils.task_helpers import _set_periodicity, _save_task, _body_set_date


@dp.message_handler(state=TaskStateGroup.text)
async def _process_text(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['text'] = message.text
    await TaskStateGroup.date.set()
    await _select_date(message)


@dp.callback_query_handler(simple_cal_callback.filter(), state=TaskStateGroup.date)
async def _process_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await _body_set_date(callback_query, callback_data, state)
    async with state.proxy() as data:
        data['date'] = date.strftime("%d.%m.%Y")
    if selected:
        await callback_query.message.answer('At what time should the task be done?\nPlease enter in format '
                                            f'H:M.')
        await TaskStateGroup.time.set()


@dp.message_handler(state=TaskStateGroup.time)
async def _process_time(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        input_time = datetime.strptime(message.text, '%H:%M').time()
        input_date = datetime.strptime(data['date'], '%d.%m.%Y').date()
        if datetime.now().date() == input_date and datetime.now().time() > input_time:
            await message.answer(_("Selected time is earlier than current time. Please select a later time."))
            return
        else:
            async with state.proxy() as data:
                data['time'] = input_time
            await TaskStateGroup.periodicity.set()
            await message.answer("Do you want to set a periodicity?", reply_markup=get_yes_no_inline_markup())
    except ValueError:
        await message.answer(_("Incorrect time format. Please enter in format hh:mm."))


@dp.callback_query_handler(lambda callback_query: callback_query.data in ['yes', 'no'],
                           state=TaskStateGroup.periodicity)
async def _process_periodicity(callback_query: CallbackQuery, state: FSMContext, user: User):
    await callback_query.message.delete()
    if callback_query.data == 'yes':
        await callback_query.message.answer(_('Enter the frequency of your task in the format Xy Xm Xw Xd, where X is '
                                              'a number (for example, 1y 1m 1w 1d) or enter "no" for a '
                                              'non-periodic task.'))
        await TaskStateGroup.periodicity.set()
    elif callback_query.data == 'no':
        await callback_query.message.answer(_('OK, periodicity will not be set.'))
        async with state.proxy() as data:
            data['periodicity'] = 'no'
        await _view_task(callback_query.message, await _save_task(callback_query.message, state, user, 'add'), 'add', '')


@dp.message_handler(state=TaskStateGroup.periodicity)
async def _process_periodicity_text(message: Message, state: FSMContext, user: User):
    task_periodicity = message.text.strip()
    if task_periodicity == 'no':
        async with state.proxy() as data:
            data['periodicity'] = task_periodicity
        await _view_task(message, await _save_task(message, state, user, 'add'), 'add', '')
    else:
        try:
            td = await _set_periodicity(task_periodicity)
            async with state.proxy() as data:
                data['periodicity'] = td
        except:
            await message.answer(_('Invalid periodicity format. Please enter the correct format (for '
                                   'example, 1y 1m 1w 1d) or enter "no" for a non-periodic task.'))
            return
        await _view_task(message, await _save_task(message, state, user, 'add'), 'add', '')


# @dp.message_handler(state=TaskStateGroup.files)
# async def files_handler(message: Message, state: FSMContext, user: User) -> None:
#     async with state.proxy() as data:
#         if document := message.document:
#             await document.download(
#                 destination_file=f"{data['file_name']}",
#             )
#         upload_file_on_drive(user.id, data['text'][0], data['file_name'])
#     await message.answer(text=_('File downloaded successfully'))
#     await _view_task(message, await _save_task(message, state, user, 'add'), 'add', '')
#
