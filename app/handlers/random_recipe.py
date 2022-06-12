from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.utility.send_photo import send_photo


@dp.message_handler(lambda message: message.text == 'Random recipe', state='*')
async def random_recipe(message: types.Message, state: FSMContext):
    recipe, photo = bd.get_random_recipe()
    await send_photo(message.chat['id'], photo)
    await message.answer(recipe)
