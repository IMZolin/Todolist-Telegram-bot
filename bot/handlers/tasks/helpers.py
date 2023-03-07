from aiogram.types import Message, CallbackQuery
from loader import dp, _
from aiogram_calendar import simple_cal_callback, SimpleCalendar


@dp.message_handler(commands=['date'])
async def _select_time(message: Message):
    text = _('Please select a date: ')
    await message.answer(text, reply_markup=await SimpleCalendar().start_calendar())


# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        text = _('You selected ')
        await callback_query.message.answer(
            f'{text} {date.strftime("%d/%m/%Y")}'
        )