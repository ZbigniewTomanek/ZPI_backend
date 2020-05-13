from django.db import models
from django.contrib.auth.models import User


class Chef(models.Model):
    name = models.CharField(max_length=150)
    url = models.CharField(max_length=500)

    def __str__(self):
        return f'Chef nr {self.id}, {self.name}'


class Ingredient(models.Model):
    url = models.CharField(max_length=100)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'Ingredient nr {self.id}, {self.name}'


class Recipe(models.Model):
    """
    time is stored in minutes
    """
    url = models.CharField(max_length=500)

    preparation_time = models.IntegerField(null=True)
    cooking_time = models.IntegerField(null=True)

    preparation_time_text = models.CharField(max_length=100, null=True)
    cooking_time_text = models.CharField(max_length=100, null=True)

    description = models.CharField(max_length=4000, null=True)

    chefs = models.ManyToManyField(Chef)

    ingredients = models.ManyToManyField(Ingredient)
    added_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Recipe nr {self.id}, {self.url}'


class IngredientsSegment(models.Model):
    title = models.CharField(max_length=4000)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'Ingredient segment nr {self.id}'


class MealIngredient(models.Model):
    ingredient_and_amount_text = models.CharField(max_length=300)
    ingredient_segment = models.ForeignKey(IngredientsSegment, on_delete=models.CASCADE)

    def __str__(self):
        return f'Meal ingredient nr {self.id}, {self.ingredient_and_amount_text}'


class Image(models.Model):
    description = models.CharField(max_length=1000)
    url = models.CharField(max_length=500)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'Image nr {self.id}, {self.url}'


class RecipesUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    liked_ingredients = models.ManyToManyField(Ingredient, related_name='%(class)s_liked_ingredient')
    disliked_ingredients = models.ManyToManyField(Ingredient, related_name='%(class)s_disliked_ingredient')
    saved_recipes = models.ManyToManyField(Recipe)

    def __str__(self):
        return str(self.user)


