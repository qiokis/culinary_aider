from app import dp
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.keyboards.default.menu import get_menu


@dp.message_handler(commands='start', state='*')
async def handler(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Ok', reply_markup=get_menu())
