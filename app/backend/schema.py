import graphene
from graphene_django import DjangoObjectType
from .models import *


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe


class ChefType(DjangoObjectType):
    class Meta:
        model = Chef


class IngredientsSegmentType(DjangoObjectType):
    class Meta:
        model = IngredientsSegment


class MealIngredientType(DjangoObjectType):
    class Meta:
        model = MealIngredient


class ImageType(DjangoObjectType):
    class Meta:
        model = Image


class Query(object):
    all_ingredients = graphene.List(IngredientType)
    ingredient = graphene.Field(IngredientType,
                                id=graphene.Int(),
                                name=graphene.String())

    all_recipes = graphene.List(RecipeType)
    recipe = graphene.Field(RecipeType,
                            id=graphene.Int())

    all_chefs = graphene.List(ChefType)
    chef = graphene.Field(ChefType,
                          id=graphene.Int(),
                          name=graphene.String())

    all_ingredients_segments = graphene.List(IngredientsSegmentType)
    ingredients_segment = graphene.Field(IngredientsSegmentType,
                                         id=graphene.Int(), )

    all_meal_ingredients = graphene.List(MealIngredientType)
    meal_ingredient = graphene.Field(MealIngredientType,
                                     id=graphene.Int(), )

    all_images = graphene.List(ImageType)
    image = graphene.Field(ImageType,
                           id=graphene.Int(), )

    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Ingredient.objects.get(pk=id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        return None

    def resolve_all_recipes(self, info, **kwargs):
        return Recipe.objects.all()

    def resolve_recipe(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Recipe.objects.get(pk=id)

        if name is not None:
            return Recipe.objects.get(name=name)

        return None

    def resolve_all_chefs(self, info, **kwargs):
        return Chef.objects.all()

    def resolve_chef(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Chef.objects.get(pk=id)

        if name is not None:
            return Chef.objects.get(name=name)

        return None

    def resolve_all_ingredients_segements(self, info, **kwargs):
        return IngredientsSegment.objects.select_related('recipe').all()

    def resolve_ingredients_segemnt(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return IngredientsSegment.objects.get(pk=id)

        return None

    def resolve_all_meal_ingredients(self, info, **kwargs):
        return MealIngredient.objects.select_related('ingredient_segment').all()

    def resolve_meal_ingredient(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return MealIngredient.objects.get(pk=id)

        return None

    def resolve_all_images(self, info, **kwargs):
        return Image.objects.select_related('recipe').all()

    def resolve_image(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Image.objects.get(pk=id)

        return None
