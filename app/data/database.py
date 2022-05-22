import random
from datetime import datetime

import psycopg2
from psycopg2.extras import NamedTupleCursor
from contextlib import closing

from app.utility.format_recipe import format_recipe
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

    def get_by_name(self, name: str) -> str:
        query = f'select * from recipe where name = \'{name.lower()}\''
        data = self._exec_query(query)[0]._asdict()
        if data:
            data.update(self._get_ingredients(data['id']))
            data.update(self._get_nationality(data['id_nationality']))
        return format_recipe(data) if data else c.NOT_FOUND_MESSAGE

    def get_by_id(self, id_: int) -> str:
        query = f'select * from recipe where id = \'{id_}\''
        data = self._exec_query(query)[0]._asdict()
        if data:
            data.update(self._get_ingredients(data['id']))
            data.update(self._get_nationality(data['id_nationality']))
        return format_recipe(data) if data else c.NOT_FOUND_MESSAGE

    def get_random_recipe(self) -> str:
        first_value = 1
        last_value = self._exec_query('select last_value from recipe_id_seq')[0].last_value
        for _ in range(c.RANDOM_ACCESS_ATTEMPTS):
            id_ = random.randint(first_value, last_value)
            recipe = self.get_by_id(id_)
            if recipe != c.NOT_FOUND_MESSAGE:
                return recipe

    def get_by_time(self, time: datetime.time):
        query = f'select * from recipe where cook_time <= \'{time}\''
        data = [recipe._asdict() for recipe in self._exec_query(query)]
        if not data:
            return c.NOT_FOUND_MESSAGE
        for recipe in data:
            recipe.update(self._get_ingredients(recipe['id']))
            recipe.update(self._get_nationality(recipe['id_nationality']))
        data = [format_recipe(recipe) for recipe in data]
        return data

    def get_by_serving_count(self, serving_number: int):
        query = f'select * from recipe where serving_number = \'{serving_number}\''
        data = [recipe._asdict() for recipe in self._exec_query(query)]
        if not data:
            return c.NOT_FOUND_MESSAGE
        for recipe in data:
            recipe.update(self._get_ingredients(recipe['id']))
            recipe.update(self._get_nationality(recipe['id_nationality']))
        data = [format_recipe(recipe) for recipe in data]
        return data