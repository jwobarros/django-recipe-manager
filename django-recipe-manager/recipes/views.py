from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)

from recipes.models import Ingredient, IngredientPrice, Recipe, RecipeIngredient
from recipes.serializers import (
    IngredientSerializer,
    IngredientPriceSerializer,
    RecipeSerializer,
    RecipeIngredientSerializer,
)

from recipes.permissions import (
    IsIngredientOwnerAndIsAuthenticated,
    IsRecipeOwnerAndIsAuthenticated,
)


class BaseIngredientView:
    serializer_class = IngredientSerializer

    def get_queryset(self):
        # return Ingredient list for current user
        return Ingredient.objects.filter(user=self.request.user)


class IngredientListCreateAPIView(BaseIngredientView, ListCreateAPIView):
    pass


class IngredientUpdateAPIView(BaseIngredientView, RetrieveUpdateAPIView):
    pass


class IngredientDestroyAPIView(BaseIngredientView, RetrieveDestroyAPIView):
    pass


class BaseIngredientPriceView:
    serializer_class = IngredientPriceSerializer
    permission_classes = [
        IsIngredientOwnerAndIsAuthenticated,
    ]

    def get_queryset(self):
        # return Price list for ingredient
        ingredients = IngredientPrice.objects.filter(
            ingredient__user=self.request.user, ingredient=self.kwargs["ingredient_pk"]
        )
        return ingredients


class IngredientPriceListCreateAPIView(BaseIngredientPriceView, ListCreateAPIView):
    pass


class IngredientPriceUpdateAPIView(BaseIngredientPriceView, RetrieveUpdateAPIView):
    pass


class IngredientPriceDestroyAPIView(BaseIngredientPriceView, RetrieveDestroyAPIView):
    pass


class BaseRecipeView:
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # return Recipe list for current user
        return Recipe.objects.filter(user=self.request.user)


class RecipeListCreateAPIView(BaseRecipeView, ListCreateAPIView):
    pass


class RecipeUpdateAPIView(BaseRecipeView, RetrieveUpdateAPIView):
    pass


class RecipeDestroyAPIView(BaseRecipeView, RetrieveDestroyAPIView):
    pass


class BaseRecipeIngredientView:
    serializer_class = RecipeIngredientSerializer
    permission_classes = [
        IsRecipeOwnerAndIsAuthenticated,
    ]

    def get_queryset(self):
        # return RecipeIngredient list for current recipe
        return RecipeIngredient.objects.filter(
            recipe__user=self.request.user, recipe=self.kwargs["recipe_pk"]
        )


class RecipeIngredientListCreateAPIView(BaseRecipeIngredientView, ListCreateAPIView):
    pass


class RecipeIngredientUpdateAPIView(BaseRecipeIngredientView, RetrieveUpdateAPIView):
    pass


class RecipeIngredientDestroyAPIView(BaseRecipeIngredientView, RetrieveDestroyAPIView):
    pass
