from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from recipes.models import Ingredient, IngredientPrice


class IngredientViewsTestCase(APITestCase):
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
        ingredient = Ingredient.objects.create(
            name="Flour",
            description="Fine wheat flour",
            article_number=12345,
            measurement="kg",
            user=self.user,
        )
        url = reverse("ingredient_update", kwargs={"pk": ingredient.pk})
        data = {
            "name": "Flour",
            "description": "Fine wheat flour updated",
            "article_number": 1234567,
            "measurement": "kg",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_ingredient(self):
        ingredient = Ingredient.objects.create(
            name="Flour",
            description="Fine wheat flour",
            article_number=12345,
            measurement="kg",
            user=self.user,
        )
        url = reverse("ingredient_delete", kwargs={"pk": ingredient.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class IngredientPriceViewsTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_authenticate(self.user)
        self.ingredient = Ingredient.objects.create(
            name="Flour",
            description="Fine wheat flour",
            article_number=12345,
            measurement="kg",
            user=self.user,
        )
        self.ingredient_price = IngredientPrice.objects.create(
            ingredient=self.ingredient,
            price=1.5,
        )

    def test_get_ingredient_prices(self):
        url = reverse(
            "ingredient_price_list_create",
            kwargs={
                "ingredient_pk": self.ingredient.pk,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ingredient_price(self):
        url = reverse(
            "ingredient_price_list_create",
            kwargs={
                "ingredient_pk": self.ingredient.pk,
            },
        )
        data = {"price": 2.5, "measurement": "kg"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["price"], data["price"])

    def test_update_ingredient_price(self):
        url = reverse(
            "ingredient_price_update",
            kwargs={
                "ingredient_pk": self.ingredient.pk,
                "pk": self.ingredient_price.pk,
            },
        )
        data = {"price": 2.5, "measurement": "kg"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_ingredient_price__wrong_user(self):
        wrong_user = get_user_model().objects.create_user(
            username="wrong_user",
            password="wrong_user",
        )
        url = reverse(
            "ingredient_price_update",
            kwargs={
                "ingredient_pk": self.ingredient.pk,
                "pk": self.ingredient_price.pk,
            },
        )
        data = {"price": 2.5, "measurement": "kg"}
        self.client.force_authenticate(wrong_user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ingredient_price(self):
        url = reverse(
            "ingredient_price_delete",
            kwargs={
                "ingredient_pk": self.ingredient.pk,
                "pk": self.ingredient_price.pk,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
