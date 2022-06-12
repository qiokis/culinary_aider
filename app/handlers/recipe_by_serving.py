from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.menu_state import MenuState
from app.utility.send_photo import send_photo


@dp.message_handler(lambda message: message.text == 'By serving count', state='*')
async def request_recipe_serving(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_serving_count)
    await message.answer('Type recipe\'s serving count')


@dp.message_handler(state=MenuState.by_serving_count)
async def get_recipe_by_serving(message: types.Message, state: FSMContext):
    try:
        count = int(message.text.lower())
    except ValueError:
        await message.answer('Wrong serving count format, please try again.')
        await request_recipe_serving(message, state)
        return
    recipes = bd.get_by_serving_count(count)
    if isinstance(recipes, str):
        await message.answer(recipes)
    else:
        for recipe, photo in recipes:
            await send_photo(message.chat['id'], photo)
            await message.answer(recipe)
