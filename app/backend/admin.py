from django.contrib import admin
from .models import *

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Image)
admin.site.register(IngredientsSegment)
admin.site.register(Chef)
admin.site.register(MealIngredient)
admin.site.register(RecipesUser)
admin.site.register(PreparationStep)
