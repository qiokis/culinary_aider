from aiogram.dispatcher.filters.state import State, StatesGroup


class MenuState(StatesGroup):
    by_ingredients = State()
    by_nationality = State()
    by_time = State()
    by_name = State()
    by_serving_count = State()


