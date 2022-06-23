from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_options():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    set_match = KeyboardButton('Match')
    set_limit = KeyboardButton('Limit')
    clear = KeyboardButton('Clear')
    show = KeyboardButton('Show')

    keyboard.add(set_match, set_limit, clear, show)
    return keyboard
