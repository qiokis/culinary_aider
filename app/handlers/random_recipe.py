from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.state_worker import update_recipe_idx
from app.handlers.general import send_recipes


@dp.message_handler(lambda message: message.text == 'Random recipe', state='*')
async def random_recipe(message: types.Message, state: FSMContext):
    await update_recipe_idx(message, state, bd.get_random_recipe())
    await send_recipes(message, state)
