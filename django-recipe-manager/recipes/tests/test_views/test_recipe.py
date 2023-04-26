from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from recipes.models import Recipe, RecipeIngredient, Ingredient


class RecipeViewsTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_authenticate(self.user)

    def test_get_ingredients(self):
        url = reverse("ingredient_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ingredient(self):
        url = reverse("ingredient_list_create")
        data = {
            "name": "test name",
            "description": "test description",
            "article_number": 1234567,
            "measurement": "pc",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["article_number"], data["article_number"])

    def test_update_ingredient(self):
        recipe = Recipe.objects.create(
            name="Carrot Cake",
            description="A delicious carrot cake",
            user=self.user,
        )
        url = reverse("recipe_update", kwargs={"pk": recipe.pk})
        data = {
            "name": "Flour",
            "description": "Fine wheat flour updated",
            "article_number": 1234567,
            "measurement": "kg",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_ingredient(self):
        recipe = Recipe.objects.create(
            name="Carrot Cake",
            description="A delicious carrot cake",
            user=self.user,
        )
        url = reverse("recipe_delete", kwargs={"pk": recipe.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RecipeIngredientViewsTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_authenticate(self.user)
        self.recipe = Recipe.objects.create(
            name="Carrot Cake",
            description="A delicious carrot cake",
            user=self.user,
        )
        self.ingredient = Ingredient.objects.create(
            name="Flour",
            description="Fine wheat flour",
            article_number=12345,
            measurement="kg",
            user=self.user,
        )

    def test_get_recipe_ingredients(self):
        url = reverse(
            "recipe_ingredient_list_create",
            kwargs={
                "recipe_pk": self.recipe.pk,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_recipe_ingredient(self):
        url = reverse(
            "recipe_ingredient_list_create",
            kwargs={
                "recipe_pk": self.recipe.pk,
            },
        )
        data = {
            "ingredient": self.ingredient.pk,
            "quantity": 2,
            "measurement": "kg",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["ingredient"], data["ingredient"])
        self.assertEqual(response.data["quantity"], data["quantity"])

    def test_update_recipe_ingredient(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe, ingredient=self.ingredient, quantity=1, measurement="kg"
        )
        url = reverse(
            "recipe_ingredient_update",
            kwargs={
                "recipe_pk": self.recipe.pk,
                "pk": recipe_ingredient.pk,
            },
        )
        data = {
            "recipe": self.recipe.pk,
            "ingredient": self.ingredient.pk,
            "quantity": 2,
            "measurement": "kg",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], data["quantity"])

    def test_update_recipe_ingredient__wrong_user(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe, ingredient=self.ingredient, quantity=1, measurement="kg"
        )
        wrong_user = get_user_model().objects.create_user(
            username="wrong_user",
            password="wrong_user",
        )
        url = reverse(
            "recipe_ingredient_update",
            kwargs={
                "recipe_pk": self.recipe.pk,
                "pk": recipe_ingredient.pk,
            },
        )
        data = {
            "ingredient": self.ingredient,
            "quantity": 2,
            "measurement": "kg",
        }
        self.client.force_authenticate(wrong_user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_recipe_ingredient(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe, ingredient=self.ingredient, quantity=1, measurement="kg"
        )
        url = reverse(
            "recipe_ingredient_delete",
            kwargs={
                "recipe_pk": self.recipe.pk,
                "pk": recipe_ingredient.pk,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
