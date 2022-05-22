from datetime import datetime

from app import dp, bd
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.menu_state import MenuState
from app.keyboards.default.menu import get_menu


@dp.message_handler(lambda message: message.text == 'By name', state='*')
async def request_recipe_name(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.by_name)
    await message.answer('Type recipe\'s name')


@dp.message_handler(state=MenuState.by_name)
async def get_recipe_by_name(message: types.Message, state: FSMContext):
    recipe = bd.get_by_name(message.text.lower())
    await message.answer(recipe)


@dp.message_handler(lambda message: message.text == 'Random recipe', state='*')
async def random_recipe(message: types.Message, state: FSMContext):
    await message.answer(bd.get_random_recipe())


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
    if isinstance(recipes, str):
        await message.answer(recipes)
    else:
        for recipe in recipes:
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
    if isinstance(recipes, str):
        await message.answer(recipes)
    else:
        for recipe in recipes:
            await message.answer(recipe)