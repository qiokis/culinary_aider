import random
from datetime import datetime

import psycopg2
from psycopg2.extras import NamedTupleCursor
from contextlib import closing

from app.utility.format_recipe import format_recipe
from app.utility.format_recipe import capitalize_first
import app.data.constants as c




class Database:

    def __init__(self, user: str, password: str, database: str, host: str, port: int) -> callable:
        self._user = user
        self._password = password
        self._database = database
        self._host = host
        self._port = port

    def _exec_query(self, query: str):
        with closing(psycopg2.connect(dbname=self._database,
                                      user=self._user,
                                      password=self._password,
                                      host=self._host,
                                      port=self._port)) as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    def _get_ingredients(self, id_recipe: int) -> dict:
        result = {'ingredients': []}
        ingredients = self._exec_query(f'select id_ingredient, id_unit, quantity'
                                       f' from recipe_ingredient where id_recipe = {id_recipe}')
        for ingredient in [ingredient._asdict() for ingredient in ingredients]:
            unit_name = None
            ingredient_name = self._exec_query(f'select name from ingredient '
                                               f'where id = {ingredient["id_ingredient"]}')[0].name
            if ingredient["id_unit"]:
                unit_name = self._exec_query(f'select name from unit '
                                             f'where id = {ingredient["id_unit"]}')[0].name
            result['ingredients'].append({'name': ingredient_name, 'unit': unit_name,
                                          'quantity': ingredient['quantity']})
        return result

    def _get_nationality(self, id_nationality: int) -> dict:
        return {'nationality':
                    self._exec_query(f'select name from nationality where id = {id_nationality}')[0].name}

    def get_by_name(self, name: str) -> set[str]:
        query = f'select * from recipe where name = \'{name.lower()}\''
        try:
            data = self._exec_query(query)[0]._asdict()
        except IndexError:
            return {'', }
        return {str(data['id']), }

    def get_by_id(self, id_: int) -> (str, str):
        query = f'select * from recipe where id = \'{id_}\''
        try:
            data = self._exec_query(query)[0]._asdict()
        except IndexError:
            return c.NOT_FOUND_MESSAGE
        return data['id']

    def get_random_recipe(self) -> (str, str):
        ids = [rec.id for rec in self._exec_query('select id from recipe')]
        id_ = random.choice(ids)
        return {str(id_), }

    def get_by_time(self, time: datetime.time) -> set[str]:
        query = f'select * from recipe where cook_time <= \'{time}\''
        data = [recipe._asdict() for recipe in self._exec_query(query)]
        if not data:
            return {'', }
        return {str(recipe['id']) for recipe in data}

    def get_by_serving_count(self, serving_number: int):
        query = f'select * from recipe where serving_number = \'{serving_number}\''
        data = [recipe._asdict() for recipe in self._exec_query(query)]
        if not data:
            return c.NOT_FOUND_MESSAGE
        return {str(recipe['id']) for recipe in data}

    def get_ingredient_id(self, ingredient_name: str):
        try:
            result = str(self._exec_query(f'select id from ingredient where name = \'{ingredient_name}\'')[0].id)
        except IndexError:
            return '-1'
        return result

    def get_by_ingredients(self, ingredients: list[str]):
        recipes = self._exec_query(f'select distinct id_recipe from recipe_ingredient'
                                   f' where id_ingredient in ({",".join(ingredients)})')
        recipes = {recipe.id_recipe: self.search_ingredients(recipe.id_recipe) for recipe in recipes}
        ingredients = {int(ingredient) for ingredient in ingredients}
        for recipe_id, ingredients_idx in recipes.items():
            if not ingredients_idx.issubset(ingredients):
                recipes[recipe_id] = {}
        answer = {str(recipe_id)
                  for recipe_id, ingredients_idx in recipes.items() if ingredients_idx}
        return answer

    def search_ingredients(self, id_recipe):
        result = self._exec_query(f'select id_ingredient from recipe_ingredient '
                         f'where id_recipe = {id_recipe}')
        result = {rec.id_ingredient for rec in result}
        return result

    def get_recipe(self, id_recipe: int):
        result = self._exec_query(f'select r.name, r.serving_number, r.cook_time, n.name as nationality,'
                                  f' instruction, photo'
                                  f' from recipe r join nationality n on n.id = id_nationality '
                                  f'where r.id = {id_recipe}')[0]._asdict()
        ingredients = self._get_ingredients(id_recipe)
        result.update(ingredients)
        return result

