from app import bd


def sort_by_ingr_quantity(recipes: list, limit: int):
    recipes = [(recipe, len(bd._get_ingredients(recipe)['ingredients'])) for recipe in recipes]
    recipes.sort(key=lambda x: x[1])
    return [recipe[0] for recipe in recipes][:limit] if limit > 0 else [recipe[0] for recipe in recipes]