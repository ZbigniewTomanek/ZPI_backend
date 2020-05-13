import graphene
from graphene_django import DjangoObjectType
from .models import *
from django.contrib.auth.models import User


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


class ClassicUserType(DjangoObjectType):
    class Meta:
        model = User


class UserType(DjangoObjectType):
    user = graphene.Field(ClassicUserType)

    class Meta:
        model = RecipesUser


class CreateUser(graphene.Mutation):
    class Arguments:
        password = graphene.String()
        username = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    def mutate(self, info, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        recipes_user = RecipesUser.objects.create(user=user)

        ok = True

        return CreateUser(user=recipes_user, ok=ok)


class AddLikedIngredient(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        ingredient_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, info, user_id, ingredient_id):
        ingredient = Ingredient.objects.get(id=ingredient_id)
        user = RecipesUser.objects.get(id=user_id)

        user.liked_ingredients.add(ingredient)

        ok = True

        return AddLikedIngredient(ok=ok)


class AddDislikedIngredient(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        ingredient_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, info, user_id, ingredient_id):
        ingredient = Ingredient.objects.get(id=ingredient_id)
        user = RecipesUser.objects.get(id=user_id)

        user.disliked_ingredients.add(ingredient)

        ok = True

        return AddDislikedIngredient(ok=ok)


class SaveUserRecipe(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        recipe_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, info, user_id, recipe_id):
        user = RecipesUser.objects.get(id=user_id)
        recipe = Recipe.objects.get(id=recipe_id)

        user.saved_recipes.add(recipe)

        ok = True

        return SaveUserRecipe(ok=ok)


class RemoveUserRecipe(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        recipe_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, info, user_id, recipe_id):
        user = RecipesUser.objects.get(id=user_id)
        recipe = Recipe.objects.get(id=recipe_id)

        user.saved_recipes.remove(recipe)

        ok = True

        return RemoveUserRecipe(ok=ok)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    add_liked_ingredient = AddLikedIngredient.Field()
    add_disliked_ingredient = AddDislikedIngredient.Field()
    save_user_recipe = SaveUserRecipe.Field()
    remove_user_recipe = RemoveUserRecipe.Field()


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

    all_users = graphene.List(UserType)
    user = graphene.Field(UserType,
                          id=graphene.Int())

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

    def resolve_all_users(self, info, **kwargs):
        return RecipesUser.objects.select_related('user').all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        username = kwargs.get('username')

        if id is not None:
            return RecipesUser.objects.get(pk=id)

        if username is not None:
            return RecipesUser.objects.get(user__username=username)

        return None
