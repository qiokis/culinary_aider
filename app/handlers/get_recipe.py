from datetime import datetime

from app import dp, bd, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.menu_state import MenuState


async def send_photo(chat_id, photo_path):
    if photo_path:
        photo = open(f'static/{photo_path}', 'rb')
        await bot.send_photo(chat_id=chat_id, photo=photo)


@dp.message_handler(lambda message: message.text == 'By name', state='*')
async def request_recipe_name(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_name)
    await message.answer('Type recipe\'s name')


@dp.message_handler(state=MenuState.by_name)
async def get_recipe_by_name(message: types.Message, state: FSMContext):
    recipe, photo_path = bd.get_by_name(message.text.lower())
    await send_photo(message.chat['id'], photo_path)
    await message.answer(recipe)


@dp.message_handler(lambda message: message.text == 'Random recipe', state='*')
async def random_recipe(message: types.Message, state: FSMContext):
    recipe, photo = bd.get_random_recipe()
    await send_photo(message.chat['id'], photo)
    await message.answer(recipe)


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
    for recipe, photo in recipes:
        await send_photo(message.chat['id'], photo)
        await message.answer(recipe)


@dp.message_handler(lambda message: message.text == 'By ingredient', state='*')
async def request_recipe_ingredients(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_ingredients)
    await message.answer('Type recipe\'s ingredients')


@dp.message_handler(state=MenuState.by_ingredients)
async def get_recipe_by_ingredients(message: types.Message, state: FSMContext):
    result = bd.get_by_ingredients(message.text)
    for recipe, photo in result:
        await send_photo(message.chat['id'], photo)
        await message.answer(recipe)