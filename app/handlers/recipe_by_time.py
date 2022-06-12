from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.menu_state import MenuState
from app.utility.message import get_selected_message
from app.utility.validators import validate_date
from app.data.state_worker import update_recipe_idx


@dp.message_handler(lambda message: message.text == 'By time', state='*')
async def request_recipe_time(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_time)
    await message.answer('Type recipe\'s cook time (Format hours:minutes)')


@dp.message_handler(state=MenuState.by_time)
async def get_recipe_by_time(message: types.Message, state: FSMContext):
    time_ = validate_date(message.text, '%H:%M')
    if time_ is False:
        await message.answer('Wrong time format, please try again.')
        await request_recipe_time(message, state)
        return
    recipes_count = await update_recipe_idx(state, bd.get_by_time(time_))
    await message.answer(get_selected_message(recipes_count))
