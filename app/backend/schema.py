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


class PreparationStepType(DjangoObjectType):
    class Meta:
        model = PreparationStep


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
        user = RecipesUser.objects.get(user_id=user_id)

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
        user = RecipesUser.objects.get(user_id=user_id)

        user.disliked_ingredients.add(ingredient)

        ok = True

        return AddDislikedIngredient(ok=ok)


class SaveUserRecipe(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        recipe_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, info, user_id, recipe_id):
        user = RecipesUser.objects.get(user_id=user_id)
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
        user = RecipesUser.objects.get(user_id=user_id)
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


def _paginate_query(queryset, first, offset, skip):
    if skip:
        queryset = queryset[skip:]

    if first and offset:
        queryset = queryset[offset:offset + first]
    else:
        if first:
            queryset = queryset[:first]

    return queryset


class Query(object):
    all_ingredients = graphene.List(IngredientType,
                                    search=graphene.String(),
                                    first=graphene.Int(),
                                    skip=graphene.Int(),
                                    offset=graphene.Int()
                                    )
    ingredient = graphene.Field(IngredientType,
                                id=graphene.Int(),
                                name=graphene.String(),
                                )

    all_recipes = graphene.List(RecipeType,
                                search=graphene.String(),
                                first=graphene.Int(),
                                skip=graphene.Int(),
                                offset=graphene.Int(),
                                liked_ingredients_ids=graphene.List(graphene.Int),
                                disliked_ingredients_ids=graphene.List(graphene.Int),
                                )
    recipe = graphene.Field(RecipeType,
                            id=graphene.Int())

    all_chefs = graphene.List(ChefType,
                              search=graphene.String(),
                              first=graphene.Int(),
                              skip=graphene.Int(),
                              offset=graphene.Int()
                              )
    chef = graphene.Field(ChefType,
                          id=graphene.Int(),
                          name=graphene.String())

    all_ingredients_segments = graphene.List(IngredientsSegmentType,
                                             search=graphene.String(),
                                             first=graphene.Int(),
                                             skip=graphene.Int(),
                                             offset=graphene.Int()
                                             )
    ingredients_segment = graphene.Field(IngredientsSegmentType,
                                         id=graphene.Int(), )

    all_meal_ingredients = graphene.List(MealIngredientType,
                                         search=graphene.String(),
                                         first=graphene.Int(),
                                         skip=graphene.Int(),
                                         offset=graphene.Int()
                                         )
    meal_ingredient = graphene.Field(MealIngredientType,
                                     id=graphene.Int(), )

    all_images = graphene.List(ImageType,
                               search=graphene.String(),
                               first=graphene.Int(),
                               skip=graphene.Int(),
                               offset=graphene.Int()
                               )
    image = graphene.Field(ImageType,
                           id=graphene.Int(), )

    all_users = graphene.List(UserType,
                              search=graphene.String(),
                              first=graphene.Int(),
                              skip=graphene.Int(),
                              offset=graphene.Int()
                              )
    user = graphene.Field(UserType,
                          id=graphene.Int())

    all_preparation_steps = graphene.List(PreparationStepType,
                                          search=graphene.String(),
                                          first=graphene.Int(),
                                          skip=graphene.Int(),
                                          offset=graphene.Int()
                                          )
    preparation_step = graphene.Field(PreparationStepType,
                                      id=graphene.Int())

    def resolve_all_ingredients(self, info, search=None, first=None, skip=None, offset=None, **kwargs):
        qs = Ingredient.objects.all()
        if search is not None:
            qs = qs.filter(name__icontains=search)

        return _paginate_query(qs, first, offset, skip)

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Ingredient.objects.get(pk=id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        return None

    def resolve_all_recipes(self, info, search=None, first=None, skip=None, offset=None,
                            liked_ingredients_ids=None, disliked_ingredients_ids=None, **kwargs):
        qs = Recipe.objects.all()

        if search is not None:
            qs = qs.filter(title__icontains=search)

        if liked_ingredients_ids is not None:
            qs = qs.filter(ingredients__in=liked_ingredients_ids).distinct()

        if disliked_ingredients_ids is not None:
            qs = qs.exclude(ingredients__in=disliked_ingredients_ids).distinct()

        return _paginate_query(qs, first, offset, skip)

    def resolve_recipe(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Recipe.objects.get(pk=id)

        if name is not None:
            return Recipe.objects.get(name=name)

        return None

    def resolve_all_chefs(self, info, search=None, first=None, skip=None, offset=None, **kwargs):
        qs = Chef.objects.all()
        if search is not None:
            qs = qs.filter(name__icontains=search)

        return _paginate_query(qs, first, offset, skip)

    def resolve_chef(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Chef.objects.get(pk=id)

        if name is not None:
            return Chef.objects.get(name=name)

        return None

    def resolve_all_ingredients_segements(self, info, search=None, first=None, skip=None, offset=None, **kwargs):
        qs = IngredientsSegment.objects.select_related('recipe').all()

        if search is not None:
            qs = qs.filter(title__icontains=search)

        return _paginate_query(qs, first, offset, skip)

    def resolve_ingredients_segemnt(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return IngredientsSegment.objects.get(pk=id)

        return None

    def resolve_all_meal_ingredients(self, info, first=None, skip=None, offset=None, **kwargs):
        qs = MealIngredient.objects.select_related('ingredient_segment').all()

        return _paginate_query(qs, first, offset, skip)

    def resolve_meal_ingredient(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return MealIngredient.objects.get(pk=id)

        return None

    def resolve_all_images(self, info, search=None, first=None, skip=None, offset=None, **kwargs):
        qs = Image.objects.all()
        if search is not None:
            qs = qs.filter(description__icontains=search)

        return _paginate_query(qs, first, offset, skip)

    def resolve_image(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Image.objects.get(pk=id)

        return None

    def resolve_all_users(self, info, search=None, first=None, skip=None, offset=None, **kwargs):
        qs = RecipesUser.objects.all()
        if search is not None:
            qs = qs.filter(description__icontains=search)

        return _paginate_query(qs, first, offset, skip)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return RecipesUser.objects.get(user_id=id)

        return None

    def resolve_all_preparation_steps(self, info, search=None, first=None, skip=None, offset=None, **kwargs):
        qs = PreparationStep.objects.all()
        if search is not None:
            qs = qs.filter(step_text__icontains=search)

        return _paginate_query(qs, first, offset, skip)

    def resolve_preparation_step(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return PreparationStep.objects.get(user_id=id)

        return None
