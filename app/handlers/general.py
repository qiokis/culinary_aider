from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.keyboards.default.menu import get_menu
from app.data.state_worker import get_recipes
from app.utility.format_recipe import format_recipe
from app.utility.send_photo import send_photo


@dp.message_handler(commands='start', state='*')
async def handler(message: types.Message, state: FSMContext):
    await state.reset_state()
    await state.update_data(recipe_idx='')
    await message.answer('Hello, let\'s cook something tasty', reply_markup=get_menu())


@dp.message_handler(commands='done', state='*')
async def send_recipes(message: types.Message, state: FSMContext):
    recipes = await get_recipes(state)
    if not recipes:
        await message.answer('No selected dishes.')
    for recipe_id in recipes:
        recipe = bd.get_recipe(recipe_id)
        await send_photo(message.chat.id, recipe['photo'])
        await message.answer(format_recipe(recipe))
    await state.reset_state()
    await state.update_data(recipe_idx='')

