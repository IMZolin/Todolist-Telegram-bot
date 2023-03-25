from aiogram.dispatcher.filters.state import StatesGroup, State


class TaskStateGroup(StatesGroup):
    text = State()
    date = State()
    time = State()
    periodicity = State()


class EditTaskStateGroup(StatesGroup):
    inlineMenu = State()
    task_id = State()
    text = State()
    date = State()
    time = State()
    periodicity = State()


class ToDoTaskStateGroup(StatesGroup):
    chooseTask = State()
    isDone = State()
    delete = State()
    edit = State()


class CompletedTaskStateGroup(StatesGroup):
    chooseTask = State()
    isDone = State()
    delete = State()
    delete_all = State()