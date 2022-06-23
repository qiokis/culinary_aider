import asyncio

from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.keyboards.default.menu import get_menu
from app.keyboards.default.options import get_options
from app.data.state_worker import get_recipes
from app.utility.format_recipe import format_recipe
from app.utility.send_photo import send_photo
from app.utility.sort_recipes import sort_by_ingr_quantity


@dp.message_handler(commands='start', state='*')
async def handler(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    await state.update_data(recipe_idx='')
    conditions = await state.get_data()
    if not conditions.get('match'):
        await state.update_data(match='-1')
    if not conditions.get('limit'):
        await state.update_data(limit='-1')
    await message.answer('Hello, let\'s cook something tasty', reply_markup=get_menu())


@dp.message_handler(commands='options', state='*')
async def options(message: types.Message, state: FSMContext):
    await message.answer('Let\'s setup ', reply_markup=get_options())


@dp.message_handler(commands='secret', state='*')
async def secret(message: types.Message, state: FSMContext):
    await message.answer('Haha gotcha, here\'s nothing')
    await asyncio.sleep(2)
    await message.answer('Hmm you still here')
    await asyncio.sleep(2)
    await message.answer('Well, you deserve it. Enjoy...')
    with open('static/secret.webm', 'rb') as vid:
        await message.answer_video_note(vid)


@dp.message_handler(commands='done', state='*')
async def send_recipes(message: types.Message, state: FSMContext):
    recipes = await get_recipes(state)
    if not recipes:
        await message.answer('No selected dishes.')
        return
    for recipe_id in sort_by_ingr_quantity(recipes, int((await state.get_data())['limit'])):
        recipe = bd.get_recipe(recipe_id)
        await send_photo(message.chat.id, recipe['photo'])
        await message.answer(format_recipe(recipe))
    await state.reset_state(with_data=False)
    await state.update_data(recipe_idx='')

