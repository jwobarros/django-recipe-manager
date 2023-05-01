from django.conf import settings
from django.db import models


MEASUREMENT_CHOICES = (
    ("pc", "Piece"),
    ("g", "gram"),
    ("kg", "kilogram"),
    ("lb", "Pound"),
    ("oz", "Ounce"),
    ("cl", "Centiliter"),
    ("ml", "Milliliter"),
    ("l", "Liter"),
    ("fl. oz", "Fluid Ounce"),
    ("gal", "Gallon"),
    ("in", "Inch"),
    ("ft", "Foot"),
    ("yd", "Yard"),
    ("mi", "Mile"),
    ("cm", "Centimeter"),
    ("m", "Meter"),
    ("km", "Kilometer"),
)


class Ingredient(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    article_number = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    measurement = models.CharField(max_length=10, choices=MEASUREMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.name


class IngredientPrice(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, related_name="ingredient", on_delete=models.CASCADE
    )
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ingredient.name


class Recipe(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="recipe_user",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="recipe", on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, related_name="recipe_ingredient", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    measurement = models.CharField(max_length=10, choices=MEASUREMENT_CHOICES)

    def __str__(self):
        return self.recipe.name
