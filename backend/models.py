from django.db import models


class Chef(models.Model):
    name = models.CharField(max_length=150)
    url = models.CharField(max_length=500)


class Ingredient(models.Model):
    url = models.CharField(max_length=100)
    name = models.CharField(max_length=200)


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


class IngredientsSegment(models.Model):
    title = models.CharField(max_length=4000)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class MealIngredient(models.Model):
    ingredient_and_amount_text = models.CharField(max_length=300)
    ingredient_segment = models.ForeignKey(IngredientsSegment, on_delete=models.CASCADE)


class Image(models.Model):
    description = models.CharField(max_length=1000)
    url = models.CharField(max_length=500)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

