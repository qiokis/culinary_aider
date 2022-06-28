from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.menu_state import MenuState
from app.utility.message import get_selected_message
from app.utility.validators import validate_ingredients
from app.data.state_worker import update_recipe_idx


@dp.message_handler(lambda message: message.text == 'By ingredient', state='*')
async def request_recipe_ingredients(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_ingredients)
    await message.answer('Type recipe\'s ingredients')


@dp.message_handler(state=MenuState.by_ingredients)
async def get_recipe_by_ingredients(message: types.Message, state: FSMContext):
    ingredients, not_found_ingredients = validate_ingredients(message.text.lower())
    if not_found_ingredients:
        await message.answer(
            f'The following ingredients were '
            f'not found: {", ".join(not_found_ingredients)}.'
            f' They will not be taken into account.'
        )
    if ingredients is False:
        await message.answer('Wrong ingredients format, please try again.')
        await request_recipe_ingredients(message, state)
        return
    recipes_count = await update_recipe_idx(message, state, bd.get_by_ingredients(ingredients,
                                                                                  int((await state.get_data())['match'])))
    await message.answer(get_selected_message(recipes_count))