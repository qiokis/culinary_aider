from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.menu_state import MenuState
from app.utility.validators import validate_int_number
from app.data.state_worker import update_recipe_idx
from app.utility.message import get_selected_message


@dp.message_handler(lambda message: message.text == 'By serving count', state='*')
async def request_recipe_serving(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_serving_count)
    await message.answer('Type recipe\'s serving count. '
                         'Remember that recipes with a multiple of the serving number'
                         ' entered by you will also be selected, but you will have to eat more :)')


@dp.message_handler(state=MenuState.by_serving_count)
async def get_recipe_by_serving(message: types.Message, state: FSMContext):
    count = validate_int_number(message.text.lower())
    if count is False:
        await message.answer('Wrong serving count format, please try again.')
        await request_recipe_serving(message, state)
        return
    recipes_count = await update_recipe_idx(message, state, bd.get_by_serving_count(count))
    await message.answer(get_selected_message(recipes_count))
