from django.contrib.auth import get_user_model
from rest_framework import serializers
from recipes.models import (
    Ingredient,
    IngredientPrice,
    Recipe,
    RecipeIngredient,
    MEASUREMENT_CHOICES,
)
from recipes.utils import convert_measurement, UnsupportedUnitConvertion
from collections import OrderedDict

from rest_framework import serializers


class AsymetricRelatedField(serializers.PrimaryKeyRelatedField):

    """This field returns the object details but recives just pk from requests"""

    def __init__(self, **kwargs):
        self.serializer_class = kwargs.pop("serializer_class")
        self.filter_by_user = kwargs.pop("filter_by_user") or False
        super().__init__(**kwargs)

    def get_user_field_name(self):
        # Find the user relation on the model
        for field in self.serializer_class.Meta.model._meta.get_fields():
            if field.is_relation and field.related_model == get_user_model():
                return field.related_query_name()
        return False

    def to_representation(self, value):
        return self.serializer_class(value).data

    def get_queryset(self):
        if self.queryset:
            return self.queryset
        if self.filter_by_user:
            user_field_name = self.get_user_field_name()
            if user_field_name:
                return self.serializer_class.Meta.model.objects.filter(
                    **{user_field_name: self.context["request"].user}
                )
        return self.serializer_class.Meta.model.objects.all()

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([(item.pk, self.display_value(item)) for item in queryset])

    def use_pk_only_optimization(self):
        return False

    @classmethod
    def from_serializer(cls, serializer, name=None, args=(), kwargs={}):
        if name is None:
            name = f"{serializer.__class__.name}AsymetricAutoField"

        return type(name, [cls], {"serializer_class": serializer})


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
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = IngredientPrice
        fields = ["id", "price", "ingredient", "measurement", "created_at"]

    def save(self):
        # Convert the price to the default produt measurement
        price_measurement = (
            self.fields["measurement"]
            .choices.get(self.validated_data["measurement"])
            .lower()
        )
        default_measurement = (
            self.validated_data["ingredient"].get_measurement_display().lower()
        )

        try:
            self.validated_data["price"] = convert_measurement(
                value=self.validated_data["price"],
                from_unit=price_measurement,
                to_unit=default_measurement,
                is_price_conversion=True,
            )
        except UnsupportedUnitConvertion:
            raise serializers.ValidationError(
                {
                    "measurement": f"Unsupported convertion between {price_measurement} and the default ingredient unit measurement: {default_measurement}"
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
        return Recipe.objects.get(pk=recipe_pk)

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class IngredientsByUser(AsymetricRelatedField):
    serializer_class = IngredientSerializer
    filter_by_user = True


class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    measurement = serializers.ChoiceField(choices=MEASUREMENT_CHOICES, write_only=True)
    recipe = serializers.HiddenField(default=CurrentRecipeField())
    ingredient = AsymetricRelatedField(
        serializer_class=IngredientSerializer, filter_by_user=True
    )
    cost = serializers.SerializerMethodField("get_ingredient_cost")

    def get_ingredient_cost(self, obj):
        latest_price = IngredientPrice.objects.filter(ingredient=obj.ingredient).latest(
            "created_at"
        )
        return round(latest_price.price * obj.quantity, 2)

    class Meta:
        model = RecipeIngredient
        fields = ["id", "quantity", "measurement", "ingredient", "recipe", "cost"]

    def save(self):
        # Convert the quantity to the default produt measurement
        ingredient_measurement = (
            self.fields["measurement"]
            .choices.get(self.validated_data["measurement"])
            .lower()
        )
        default_measurement = (
            self.validated_data["ingredient"].get_measurement_display().lower()
        )

        try:
            self.validated_data["quantity"] = convert_measurement(
                value=self.validated_data["quantity"],
                from_unit=ingredient_measurement,
                to_unit=default_measurement,
            )
        except UnsupportedUnitConvertion:
            raise serializers.ValidationError(
                {
                    "measurement": f"Unsupported convertion between {ingredient_measurement} and the default ingredient unit measurement: {default_measurement}"
                }
            )
        self.is_valid()
        return super().save()
