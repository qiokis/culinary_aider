def format_quantity(quantity: int | float) -> float | int:
    try:
        integer, fractional = str(quantity).split('.')
    except:
        return int(quantity)
    return float(quantity) if float(fractional) > 0 else int(integer)


def capitalize_first(text: str) -> str:
    return text[0].upper() + text[1:]


def format_recipe(recipe: dict):
    title = f'{capitalize_first(recipe["name"])}\n' \
           f'Serving number: {recipe["serving_number"]}\n' \
           f'Cook time: {recipe["cook_time"]}\n' \
           f'Nationality: {recipe["nationality"]}\n'
    ingredients = ''
    if recipe['ingredients']:
        ingredients = '\n'.join([f'{counter+1})'
                                 f'{capitalize_first(ingredient["name"])}'
                                 f' {" - "+str(format_quantity(ingredient["quantity"])) if ingredient["quantity"] else ""}'
                                 f' {ingredient["unit"] if ingredient["unit"] else ""}'
                                 for counter, ingredient in enumerate(recipe['ingredients'])])
        ingredients = f'You will need:\n{ingredients}'

    return f'{title}\n{ingredients}\n\n{recipe["instruction"]}'