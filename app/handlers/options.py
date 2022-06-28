from app import dp
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.options_state import OptionsState


@dp.message_handler(lambda message: message.text == 'Limit', state='*')
async def request_limit(message: types.Message, state: FSMContext):
    await state.set_state(OptionsState.set_limit)
    await message.answer('Type recipe\'s limit (This number represents maximum of recipes that you can get)')


@dp.message_handler(state=OptionsState.set_limit)
async def get_limit(message: types.Message, state: FSMContext):
    limit = -1
    try:
        limit = int(message.text.lower())
    except ValueError:
        await request_limit(message, state)
    await state.update_data(limit=limit)
    await message.answer(f'Limit {limit} successfully set.')
    await state.reset_state(with_data=False)


@dp.message_handler(lambda message: message.text == 'Match', state='*')
async def request_match(message: types.Message, state: FSMContext):
    await state.set_state(OptionsState.set_match)
    await message.answer('Type recipe\'s match '
                         '(This number represents minimum of ingredients'
                         ' that should match with recipe ingredients)')


@dp.message_handler(state=OptionsState.set_match)
async def get_match(message: types.Message, state: FSMContext):
    match = -1
    try:
        match = int(message.text.lower())
    except ValueError:
        await request_match(message, state)
    await state.update_data(match=match)
    await message.answer(f'Match {match} successfully set.')
    await state.reset_state(with_data=False)


@dp.message_handler(lambda message: message.text == 'Clear', state='*')
async def request_clear(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('All options cleared.')


@dp.message_handler(lambda message: message.text == 'Show', state='*')
async def request_show(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f'Limit: {data["limit"]}. Match: {data["match"]}')