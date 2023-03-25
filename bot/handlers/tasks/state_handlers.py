from bot.keyboards.default import get_default_markup
from loader import dp, _
from models import User
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data.startswith('main_menu'), state='*')
async def back_to_main_menu(callback_query: CallbackQuery, state: FSMContext, user: User) -> None:
    await callback_query.message.delete()
    text = _("You have returned to the main menu.")
    await callback_query.message.answer(text, reply_markup=get_default_markup(user))
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'cancel')
async def cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    prev_state = await state.get_state()
    await callback_query.message.delete()
    await state.reset_state(with_data=False)
    await state.set_state(prev_state)  # set state back to previous state
    await callback_query.message.answer(_('Action cancelled.'))