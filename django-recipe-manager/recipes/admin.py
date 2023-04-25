from django.contrib import admin
from recipes import models

# Register your models here.

admin.site.register(models.Ingredient)
admin.site.register(models.IngredientPrice)
admin.site.register(models.Recipe)
admin.site.register(models.RecipeIngredient)
