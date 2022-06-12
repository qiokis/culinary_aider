from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.menu_state import MenuState
from app.utility.send_photo import send_photo


@dp.message_handler(lambda message: message.text == 'By ingredient', state='*')
async def request_recipe_ingredients(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_ingredients)
    await message.answer('Type recipe\'s ingredients')


@dp.message_handler(state=MenuState.by_ingredients)
async def get_recipe_by_ingredients(message: types.Message, state: FSMContext):
    result = bd.get_by_ingredients(message.text)
    if isinstance(result, str):
        await message.answer(result)
    else:
        for recipe, photo in result:
            await send_photo(message.chat['id'], photo)
            await message.answer(recipe)
