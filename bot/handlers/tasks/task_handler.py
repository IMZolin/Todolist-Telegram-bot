from datetime import datetime, timedelta, date, time
from time import strftime, strptime
from typing import List

from aiogram.dispatcher import FSMContext

from aiogram.types import Message, CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from bot.forms.forms import TaskStateGroup
from bot.handlers.tasks.calendar import _select_date, _process_simple_calendar
from bot.keyboards.inline.task import get_yes_no_inline_markup, get_todo_inline_markup, get_completed_inline_markup
from loader import dp, _
from models import User
from models.task import Task
from services.tasks import create_task, get_tasks, get_to_do, get_completed


@dp.message_handler(i18n_text='New task 🆕')
@dp.message_handler(commands=['new_task'])
async def new_task(message: Message) -> None:
    await TaskStateGroup.text.set()
    await message.answer(_('Your new task:\nEnter description of your task'))


@dp.message_handler(i18n_text='Edit task ✏')
@dp.message_handler(commands=['edit_task'])
async def edit_task(message: Message):
    await to_do_list()
    await message.answer(_('Enter id of task'))


@dp.message_handler(i18n_text='To-do list 📃')
@dp.message_handler(commands=['todo'])
async def to_do_list(message: Message, user: User):
    tasks = get_to_do(user.id)
    await _view_tasks(message, tasks, 'to-do')


@dp.message_handler(i18n_text='Completed cases 🏆')
@dp.message_handler(commands=['completed'])
async def completed_cases(message: Message, user: User):
    tasks = get_completed(user.id)
    await _view_tasks(message, tasks, 'completed')


# Support functions
@dp.message_handler(state=TaskStateGroup.text)
async def _process_text(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['text'] = message.text
    await TaskStateGroup.date.set()
    await _select_date(message)


@dp.callback_query_handler(simple_cal_callback.filter(), state=TaskStateGroup.date)
async def _process_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await _process_simple_calendar(callback_query, callback_data)

    async with state.proxy() as data:
        data['date'] = date.strftime("%d.%m.%Y")

    while selected and await _is_input_earlier_today(date):
        await callback_query.message.answer(_("Wrong date. Please enter the day before today"),
                                            reply_markup=await SimpleCalendar().start_calendar())
        selected, date = await _process_simple_calendar(callback_query, callback_data)
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
        print(input_date)
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
    if callback_query.data == 'yes':
        await callback_query.message.answer(_('Enter the frequency of your task in the format Xd Xh Xm, where X is '
                                              'a number (for example, 1d 2h 30m)'))
        await TaskStateGroup.periodicity.set()
    elif callback_query.data == 'no':
        await callback_query.message.answer(_('OK, periodicity will not be set.'))
        async with state.proxy() as data:
            data['periodicity'] = 'no'
        await _save_task(callback_query.message, state, user)


@dp.message_handler(state=TaskStateGroup.periodicity)
async def _process_periodicity_text(message: Message, state: FSMContext, user: User):
    task_periodicity = message.text.strip()
    try:
        td = timedelta()
        parts = task_periodicity.split()
        for part in parts:
            if part[-1] == 'd':
                td += timedelta(days=int(part[:-1]))
            elif part[-1] == 'h':
                td += timedelta(hours=int(part[:-1]))
            elif part[-1] == 'm':
                td += timedelta(minutes=int(part[:-1]))
        async with state.proxy() as data:
            data['periodicity'] = task_periodicity
    except:
        await message.answer(_('Invalid periodicity format. Please enter the correct format (for '
                               'example, 1d 2h 30m) or enter "no" for a non-periodic task.'))
        return
    await _save_task(message, state, user)


async def _is_input_earlier_today(input_date):
    return datetime.now().date() > input_date.date()


async def _is_input_time_earlier_now_time(input_date, input_time: time):
    if datetime.now().date() == input_date:
        return datetime.now().time() > input_time
    else:
        return False


async def _view_tasks(message: Message, tasks: List[Task], param: str):
    if not tasks:
        await message.answer(_(f'No {param} tasks.'))
        return
    else:
        await message.answer(_(f'Your {param} list:\n'))
        for task in tasks:
            await _view_task(message, task, param)


async def _view_task(message: Message, task: Task, param: str):
    response = f"{task.id}. {task.text} - {task.date} at {task.time}"
    if task.periodicity != 'no':
        response += f", {task.periodicity}\n"
    else:
        response += "\n"
    if param == 'to-do':
        await message.answer(response, reply_markup=get_todo_inline_markup())
    elif param == 'completed':
        await message.answer(response, reply_markup=get_completed_inline_markup())


async def _save_task(message: Message, state: FSMContext, user: User):
    data = await state.get_data()
    task_text = data['text']
    task_date = data['date']
    task_time = data['time']
    task_periodicity = data.get('periodicity', None)
    create_task(user.id, task_text, task_date, task_time, task_periodicity)
    await state.finish()
    await message.answer(_('Task added successfully.'))
