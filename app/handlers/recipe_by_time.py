from datetime import datetime

from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.menu_state import MenuState
from app.utility.send_photo import send_photo


@dp.message_handler(lambda message: message.text == 'By time', state='*')
async def request_recipe_time(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_time)
    await message.answer('Type recipe\'s cook time (Format hours:minutes)')


@dp.message_handler(state=MenuState.by_time)
async def get_recipe_by_time(message: types.Message, state: FSMContext):
    try:
        time_ = datetime.strptime(message.text, '%H:%M')
    except ValueError:
        await message.answer('Wrong time format, please try again.')
        await request_recipe_time(message, state)
        return
    recipes = bd.get_by_time(time_)
    for recipe, photo in recipes:
        await send_photo(message.chat['id'], photo)
        await message.answer(recipe)
