def capitalize_first(text: str):
    return text[0].upper() + text[1:]


def format_recipe(recipe: dict):
    title = f'{capitalize_first(recipe["name"])}\n' \
           f'Serving number: {recipe["serving_number"]}\n' \
           f'Cook time: {recipe["cook_time"]}\n' \
           f'Nationality: {recipe["nationality"]}\n'
    ingredients = ''
    if recipe['ingredients']:
        ingredients = '\n'.join([f'{counter+1}) '
                                 f'{capitalize_first(ingredient["name"])} - {ingredient["quantity"]}'
                                 f' {ingredient["unit"] if ingredient["unit"] else ""}'
                                 for counter, ingredient in enumerate(recipe['ingredients'])])
        ingredients = f'You will need:\n{ingredients}'

    return f'{title}\n{ingredients}'