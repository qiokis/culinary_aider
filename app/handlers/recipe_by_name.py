from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.menu_state import MenuState
from app.data.state_worker import update_recipe_idx
from app.handlers.general import send_recipes
from app.utility.message import get_selected_message


@dp.message_handler(lambda message: message.text == 'By name', state='*')
async def request_recipe_name(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_name)
    await message.answer('Type recipe\'s name')


@dp.message_handler(state=MenuState.by_name)
async def get_recipe_by_name(message: types.Message, state: FSMContext):
    recipes_count = await update_recipe_idx(message, state, bd.get_by_name(message.text.lower()))
    if recipes_count == 0:
        await message.answer('We don\'t have such a dish. Please try another.')
        return
    elif recipes_count == 1:
        await send_recipes(message, state)
        return
    await message.answer(get_selected_message(recipes_count))
