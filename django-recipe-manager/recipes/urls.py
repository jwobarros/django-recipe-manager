from django.urls import path
from recipes import views


urlpatterns = [
    # Ingredient Views
    path(
        "ingredients/",
        views.IngredientListCreateAPIView.as_view(),
        name="ingredient_list_create",
    ),
    path(
        "ingredients/<int:pk>/",
        views.IngredientUpdateAPIView.as_view(),
        name="ingredient_update",
    ),
    path(
        "ingredients/delete/<int:pk>/",
        views.IngredientDestroyAPIView.as_view(),
        name="ingredient_delete",
    ),
    # Ingredient Price Views
    path(
        "ingredients/<int:ingredient_pk>/prices/",
        views.IngredientPriceListCreateAPIView.as_view(),
        name="ingredient_price_list_create",
    ),
    path(
        "ingredients/<int:ingredient_pk>/prices/<int:pk>/",
        views.IngredientPriceUpdateAPIView.as_view(),
        name="ingredient_price_update",
    ),
    path(
        "ingredients/<int:ingredient_pk>/prices/delete/<int:pk>/",
        views.IngredientPriceDestroyAPIView.as_view(),
        name="ingredient_price_delete",
    ),
    # Recipes views
    path(
        "recipes/",
        views.RecipeListCreateAPIView.as_view(),
        name="recipe_list_create",
    ),
    path(
        "recipes/<int:pk>/",
        views.RecipeUpdateAPIView.as_view(),
        name="recipe_update",
    ),
    path(
        "recipes/delete/<int:pk>/",
        views.RecipeDestroyAPIView.as_view(),
        name="recipe_delete",
    ),
    # Recipe Ingredient views
    path(
        "recipes/<int:recipe_pk>/ingredients/",
        views.RecipeIngredientListCreateAPIView.as_view(),
        name="recipe_ingredient_list_create",
    ),
    path(
        "recipes/<int:recipe_pk>/ingredients/<int:pk>/",
        views.RecipeIngredientUpdateAPIView.as_view(),
        name="recipe_ingredient_update",
    ),
    path(
        "recipes/<int:recipe_pk>/ingredients/delete/<int:pk>/",
        views.RecipeIngredientDestroyAPIView.as_view(),
        name="recipe_ingredient_delete",
    ),
]
