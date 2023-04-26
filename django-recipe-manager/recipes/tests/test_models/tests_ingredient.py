from django.contrib.auth import get_user_model
from django.test import TestCase
from recipes.models import Ingredient, IngredientPrice


class IngredientModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="normaluser", password="foo", email="normal@user.com"
        )
        self.ingredient = Ingredient.objects.create(
            name="Flour",
            description="Fine wheat flour",
            article_number=12345,
            measurement="kg",
            user=self.user,
        )

    def test_ingredient_name(self):
        self.assertEqual(str(self.ingredient), "Flour")

    def test_ingredient_description(self):
        self.assertEqual(self.ingredient.description, "Fine wheat flour")

    def test_ingredient_article_number(self):
        self.assertEqual(self.ingredient.article_number, 12345)

    def test_ingredient_measurement(self):
        self.assertEqual(self.ingredient.measurement, "kg")

    def test_ingredient_user(self):
        self.assertEqual(self.ingredient.user, self.user)

    def test_ingredient_created_at(self):
        self.assertIsNotNone(self.ingredient.created_at)

    def test_ingredient_unique_article_number(self):
        with self.assertRaises(Exception):
            Ingredient.objects.create(
                name="Sugar",
                article_number=12345,
                measurement="kg",
                user=self.user.id,
            )


class IngredientPriceModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="normaluser", password="foo", email="normal@user.com"
        )
        self.ingredient = Ingredient.objects.create(
            name="Flour",
            description="Fine wheat flour",
            article_number=12345,
            measurement="kg",
            user=self.user,
        )
        self.ingredient_price = IngredientPrice.objects.create(
            ingredient=self.ingredient,
            price=2.50,
        )

    def test_ingredient_price_ingredient(self):
        self.assertEqual(self.ingredient_price.ingredient, self.ingredient)

    def test_ingredient_price_price(self):
        self.assertEqual(self.ingredient_price.price, 2.50)

    def test_ingredient_price_created_at(self):
        self.assertIsNotNone(self.ingredient_price.created_at)

    def test_ingredient_price_str(self):
        self.assertEqual(str(self.ingredient_price), "Flour")
