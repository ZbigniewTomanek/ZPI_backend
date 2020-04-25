import json
import os
from .models import *
import logging
from tqdm import tqdm

_PREP_TIME_KEY = 'prep_time'
_COOK_TIME_KEY = 'cook_time'
_RECIPE_URL_KEY = 'recipe_url'
_RECIPE_DESCRIPTION_KEY = 'recipe_description'

_INGREDIENTS_SEGMENT_KEY = 'ingredient_segments'
_INGREDIENTS_SEGMENT_TITLE_KEY = 'title'

_INGREDIENTS_SEGMENT_INGREDIENTS_LIST_KEY = 'ingredients'

_LIST_OF_INGREDIENTS_KEY = 'list_of_ingredients'

_CHEF_LIST_KEY = 'chef_data_list'
_CHEF_NAME_KEY = 'chef_name'
_CHEF_LINK_KEY = 'chef_link'

_IMAGE_DATA_KEY = 'image_data'
_IMAGE_DESCRIPTION_KEY = 'image_alt_text'
_IMAGE_URL_KEY = 'image_main'

LOG = logging.getLogger(__name__)


def load_json_data(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/{filename}', 'r') as f:
        text = f.readlines()

    string = ''.join(text)
    return json.loads(string)


def get_number_in_minutes_from_text(text):
    if text is None:
        return None

    words = text.split(' ')
    numbers = []

    for word in words:
        try:
            numbers.append(int(word))
        except ValueError:
            pass

    if len(numbers) == 0:
        return None

    if any([number < 10 for number in numbers]):
        numbers = [number * 60 for number in numbers] # convert to minutes

    return int(sum(numbers) / len(numbers))


def save_meal_ingredients(ingredient_segment, meal_ingredients):
    for meal_ingredient in meal_ingredients:
        ingredient = MealIngredient.objects.create(
            ingredient_and_amount_text=meal_ingredient,
            ingredient_segment=ingredient_segment)
        ingredient.save()


def save_ingredient_segments(ingredient_segments, recipe):
    for segment in ingredient_segments:
        title = segment.get(_INGREDIENTS_SEGMENT_TITLE_KEY)
        ingredient_segment = IngredientsSegment.objects.create(title=title, recipe=recipe)
        ingredient_segment.save()

        meal_ingredients = segment.get(_INGREDIENTS_SEGMENT_INGREDIENTS_LIST_KEY)
        save_meal_ingredients(ingredient_segment, meal_ingredients)


def save_chefs(chefs, recipe):
    for chef in chefs:
        name = chef.get(_CHEF_NAME_KEY)
        url = chef.get(_CHEF_LINK_KEY)

        if Chef.objects.filter(name=name).exists():
            LOG.info(f'{chef} is already in db')
            return
        else:
            LOG.info(f'Adding {chef} to db')

        chef_o = Chef.objects.create(name=name, url=url)
        chef_o.save()

        chef_o.recipe_set.add(recipe)
        recipe.chefs.add(chef_o)


def extract_ingredient_name(url_text):
    segments = url_text.split('/')
    name = segments[-1]
    name = name.replace('_', ' ')

    return name


def save_ingredients(recipe, ingredients):
    for ingredient_url in ingredients:
        ingredient_qs = Ingredient.objects.filter(url=ingredient_url)

        if ingredient_qs.exists():
            LOG.info(f'{ingredient_url} is already in database')
            return
        else:
            LOG.info(f'Putting {ingredient_url} to database')

        name = extract_ingredient_name(ingredient_url)
        ingredient = Ingredient.objects.create(url=ingredient_url, name=name)
        ingredient.save()

        recipe.ingredients.add(ingredient)
        ingredient.recipe_set.add(recipe)


def save_image(image, recipe):
    description = image.get(_IMAGE_DESCRIPTION_KEY)
    url = image.get(_IMAGE_URL_KEY)

    img = Image.objects.create(url=url, description=description, recipe=recipe)
    img.save()


def save_recipe(recipe_dict: dict):
    prep_time_text = recipe_dict.get(_PREP_TIME_KEY)
    cook_time_text = recipe_dict.get(_COOK_TIME_KEY)

    prep_time = get_number_in_minutes_from_text(prep_time_text)
    cook_time = get_number_in_minutes_from_text(cook_time_text)

    recipe_url = recipe_dict[_RECIPE_URL_KEY]
    recipe_description = recipe_dict.get(_RECIPE_DESCRIPTION_KEY)

    recipe = Recipe.objects.create(preparation_time_text=prep_time,
                                   preparation_time=prep_time,
                                   cooking_time_text=cook_time_text,
                                   cooking_time=cook_time,
                                   url=recipe_url,
                                   description=recipe_description)

    ingredients = recipe_dict.get(_LIST_OF_INGREDIENTS_KEY)
    if ingredients is not None:
        save_ingredients(recipe, ingredients)

    ingredients_segment = recipe_dict.get(_INGREDIENTS_SEGMENT_KEY)
    if ingredients_segment is not None:
        save_ingredient_segments(ingredients_segment, recipe)

    chefs = recipe_dict.get(_CHEF_LIST_KEY)
    if chefs is not None:
        save_chefs(chefs, recipe)

    image = recipe_dict.get(_IMAGE_DATA_KEY)
    if image is not None:
        save_image(image, recipe)

    recipe.save()


def save_recipes(recipes_list):
    for recipe in tqdm(recipes_list):
        save_recipe(recipe)


def delete_all(all_models):
    for model in all_models:
        for obj in model.objects.all():
            obj.delete()


def exe():
    LOG.info('Deleting all previous data')
    delete_all([Image, Chef, MealIngredient, IngredientsSegment, Ingredient, Recipe])

    LOG.info('Loading recipes from json')
    data = load_json_data('parsed_recipes.json')
    save_recipes(data)


if __name__ == '__main__':
    exe()
