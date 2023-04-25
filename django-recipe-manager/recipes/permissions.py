from rest_framework.permissions import BasePermission
from recipes.models import Ingredient, Recipe


class IsIngredientOwnerAndIsAuthenticated(BasePermission):
    """Allow users to just create, update and delete prices to their own Ingredients."""

    def has_permission(self, request, view):
        is_ingredient_owner = (
            Ingredient.objects.get(
                pk=request.parser_context.get("kwargs").get("ingredient_pk")
            ).user
            == request.user
        )
        return bool(
            request.user and request.user.is_authenticated and is_ingredient_owner
        )


class IsRecipeOwnerAndIsAuthenticated(BasePermission):
    """Allow users to just create, update and delete ingredients to their own Recipes."""

    def has_permission(self, request, view):
        is_recipe_owner = (
            Recipe.objects.get(
                pk=request.parser_context.get("kwargs").get("recipe_pk")
            ).user
            == request.user
        )
        return bool(
            request.user and request.user.is_authenticated and is_recipe_owner
        )
