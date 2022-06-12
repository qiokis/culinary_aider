from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.menu_state import MenuState
from app.utility.message import get_selected_message
from app.utility.send_photo import send_photo
from app.utility.validators import validate_ingredients
from app.data.state_worker import update_recipe_idx


@dp.message_handler(lambda message: message.text == 'By ingredient', state='*')
async def request_recipe_ingredients(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_ingredients)
    await message.answer('Type recipe\'s ingredients')


@dp.message_handler(state=MenuState.by_ingredients)
async def get_recipe_by_ingredients(message: types.Message, state: FSMContext):
    ingredients = validate_ingredients(message.text.lower())
    if ingredients is False:
        await message.answer('Wrong ingredients format, please try again.')
        await request_recipe_ingredients(message, state)
        return
    recipes_count = await update_recipe_idx(state, bd.get_by_ingredients(ingredients))
    await message.answer(get_selected_message(recipes_count))