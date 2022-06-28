from aiogram.dispatcher.filters.state import State, StatesGroup


class OptionsState(StatesGroup):
    options = State()
    set_limit = State()
    set_match = State()


