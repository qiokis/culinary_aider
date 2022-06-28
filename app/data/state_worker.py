import re
from typing import Set

from aiogram.types import Message
from aiogram.dispatcher import FSMContext


async def update_recipe_idx(message: Message, state: FSMContext, new_idx: Set[str]) -> int:
    recipe_idx = await state.get_data()
    recipe_idx = recipe_idx['recipe_idx']
    if not isinstance(new_idx, set):
        await message.answer('Something went wrong. The filter will not be applied.')
        return len(recipe_idx.split(',')) if re.search(r'.*\d+.*', recipe_idx) else 0
    if len(recipe_idx) == 0:
        new_recipe_idx = ','.join(new_idx)
        new_len = len(new_idx)
    else:
        state_recipes = set(recipe_idx.split(','))
        recipe_intersect = state_recipes.intersection(new_idx)
        new_recipe_idx = ','.join(recipe_intersect)
        new_len = len(recipe_intersect)
    await state.reset_state(with_data=False)
    await state.update_data(recipe_idx=new_recipe_idx)
    return new_len


async def get_recipes(state: FSMContext) -> list[int] | bool:
    recipes = await state.get_data()
    recipes = recipes['recipe_idx']
    if not recipes:
        return False
    return [int(recipe) for recipe in recipes.split(',')]
