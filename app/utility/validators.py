from datetime import datetime
import re

from app import bd


def validate_int_number(number: str) -> int | bool:
    try:
        number = int(number)
    except ValueError:
        return False
    return number


def validate_date(date: str, format_: str) -> datetime | bool:
    try:
        date = datetime.strptime(date, format_)
    except ValueError:
        return False
    return date


def validate_ingredients(list_: str) -> set[str] | bool:
    if not re.search(r'^(\s*(\w+\s*)+\s*,)*(\s*\w+\s*)+$', list_):
        return False
    ingredients = list_.lower().strip()
    ingredients_idx = []
    for ingredient in ingredients.split(','):
        id_ = bd.get_ingredient_id(ingredient.strip())
        if id_ == '-1':
            continue
        ingredients_idx.append(id_)
    ingredients = ingredients_idx[:]
    ingredients.sort()
    return set(ingredients)
