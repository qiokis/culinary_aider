from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    by_name = KeyboardButton('By name')
    by_ingredient = KeyboardButton('By ingredient')
    by_time = KeyboardButton('By time')
    by_serving_count = KeyboardButton('By serving count')
    random = KeyboardButton('Random recipe')

    keyboard.add(by_name, by_ingredient, by_time, by_serving_count, random)
    return keyboard
