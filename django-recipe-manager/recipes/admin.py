from django.contrib import admin
from recipes import models

# Register your models here.

admin.site.register(models.Product)
admin.site.register(models.ProductPrice)
admin.site.register(models.Recipe)
admin.site.register(models.RecipeProduct)
