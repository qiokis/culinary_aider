from datetime import datetime

from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.menu_state import MenuState
from app.utility.send_photo import send_photo


@dp.message_handler(lambda message: message.text == 'By name', state='*')
async def request_recipe_name(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_name)
    await message.answer('Type recipe\'s name')


@dp.message_handler(state=MenuState.by_name)
async def get_recipe_by_name(message: types.Message, state: FSMContext):
    recipe, photo_path = bd.get_by_name(message.text.lower())
    await send_photo(message.chat['id'], photo_path)
    await message.answer(recipe)
