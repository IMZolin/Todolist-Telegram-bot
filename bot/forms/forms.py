from aiogram.dispatcher.filters.state import StatesGroup, State


class TaskStateGroup(StatesGroup):
    text = State()
    date = State()
    time = State()
    periodicity = State()


class UpdateTaskStateGroup(StatesGroup):
    text = State()
    date = State()
    time = State()
    periodicity = State()
    isDone = State()