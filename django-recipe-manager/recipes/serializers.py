from rest_framework import serializers
from recipes.models import (
    Ingredient,
    IngredientPrice,
    Recipe,
    RecipeIngredient,
    MEASUREMENT_CHOICES,
)
from recipes.utils import convert_price, UnsupportedUnitConvertion


class IngredientSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ingredient
        fields = ["id", "name", "description", "article_number", "measurement", "user"]


class CurrentIngredientField:
    """Helper class to return the current ingredient object"""

    requires_context = True

    def __call__(self, serializer_field):
        ingredient_pk = (
            serializer_field.context["request"]
            .parser_context.get("kwargs")
            .get("ingredient_pk")
        )
        return Ingredient.objects.get(pk=ingredient_pk)

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class IngredientPriceSerializer(serializers.HyperlinkedModelSerializer):
    measurement = serializers.ChoiceField(choices=MEASUREMENT_CHOICES, write_only=True)
    ingredient = serializers.HiddenField(default=CurrentIngredientField())

    class Meta:
        model = IngredientPrice
        fields = ["id", "price", "ingredient", "measurement"]

    def save(self):
        # Convert the price to the default produt measurement
        price_measurement = (
            self.fields["measurement"]
            .choices.get(self.validated_data["measurement"])
            .lower()
        )
        product_measurement = (
            self.validated_data["ingredient"].get_measurement_display().lower()
        )

        try:
            self.validated_data["price"] = convert_price(
                value=self.validated_data["price"],
                from_unit=price_measurement,
                to_unit=product_measurement,
            )
        except UnsupportedUnitConvertion:
            raise serializers.ValidationError(
                {
                    "measurement": f"Unsupported convertion between {price_measurement} and the default ingredient unit measurement: {product_measurement}"
                }
            )

        # removing custom field and validating the new data
        self.validated_data.pop("measurement")
        self.is_valid()
        return super().save()


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ["id", "name", "description", "user"]


class CurrentRecipeField:
    """Helper class to return the current recipe object"""

    requires_context = True

    def __call__(self, serializer_field):
        recipe_pk = (
            serializer_field.context["request"]
            .parser_context.get("kwargs")
            .get("recipe_pk")
        )
        return RecipeIngredient.objects.get(pk=recipe_pk)

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    ingredient = serializers.HiddenField(default=CurrentRecipeField())

    class Meta:
        model = RecipeIngredient
        fields = ["id", "ingredient", "quantity", "measurement"]
