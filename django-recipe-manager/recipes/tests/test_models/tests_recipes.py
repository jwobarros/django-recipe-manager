from django.contrib.auth import get_user_model
from django.test import TestCase
from recipes.models import Recipe, RecipeIngredient, Ingredient


class RecipeModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="testuser")
        self.recipe = Recipe.objects.create(
            name="Pasta Carbonara",
            description="Spaghetti with egg, pancetta, and parmesan cheese",
            user=self.user,
        )

    def test_recipe_name(self):
        self.assertEqual(str(self.recipe), "Pasta Carbonara")

    def test_recipe_description(self):
        self.assertEqual(
            self.recipe.description, "Spaghetti with egg, pancetta, and parmesan cheese"
        )

    def test_recipe_user(self):
        self.assertEqual(self.recipe.user, self.user)

    def test_recipe_created_at(self):
        self.assertIsNotNone(self.recipe.created_at)


class RecipeIngredientModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="testuser")
        self.ingredient = Ingredient.objects.create(
            name="Eggs",
            description="Fresh chicken eggs",
            article_number=12346,
            measurement="pc",
            user=self.user,
        )
        self.recipe = Recipe.objects.create(
            name="Scrambled Eggs",
            description="A classic breakfast dish",
            user=self.user,
        )
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=2,
            measurement="pc",
        )

    def test_recipe_ingredient_recipe(self):
        self.assertEqual(self.recipe_ingredient.recipe, self.recipe)

    def test_recipe_ingredient_ingredient(self):
        self.assertEqual(self.recipe_ingredient.ingredient, self.ingredient)

    def test_recipe_ingredient_quantity(self):
        self.assertEqual(self.recipe_ingredient.quantity, 2)

    def test_recipe_ingredient_measurement(self):
        self.assertEqual(self.recipe_ingredient.measurement, "pc")

    def test_recipe_ingredient_str(self):
        self.assertEqual(str(self.recipe_ingredient), "Scrambled Eggs")
