from aiogram.dispatcher.filters.state import StatesGroup, State


class TaskStateGroup(StatesGroup):
    text = State()
    date = State()
    time = State()
    periodicity = State()
    files = State()
    file_name = State()


class EditTaskStateGroup(StatesGroup):
    inlineMenu = State()
    task_id = State()
    text = State()
    date = State()
    time = State()
    periodicity = State()
