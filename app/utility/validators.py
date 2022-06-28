from datetime import datetime
import re
from typing import Tuple

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


def validate_ingredients(list_: str) -> Tuple[set[str], list] | bool:
    if not re.search(r'^(\s*(\w+\s*)+\s*,)*(\s*\w+\s*)+$', list_):
        return False
    ingredients = list_.lower().strip()
    ingredients_idx = []
    not_found_ingredients = []
    for ingredient in ingredients.split(','):
        id_ = bd.get_ingredient_id(ingredient.strip())
        if id_ == '-1':
            not_found_ingredients.append(ingredient)
            continue
        ingredients_idx.append(id_)
    ingredients = ingredients_idx[:]
    ingredients.sort()
    return set(ingredients), not_found_ingredients
