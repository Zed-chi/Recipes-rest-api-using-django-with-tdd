from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient, Recipe
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse("recipe:ingredient-list")


class PublicIngredientsApiTests(TestCase):
    """ Tests public Ingredients api """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Tests that login is required to operate with Ingredients api """
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """ Test Ingredients api with authorized user """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.ru", password="password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """ Tests gitting ingredients list """
        Ingredient.objects.create(user=self.user, name="test")
        Ingredient.objects.create(user=self.user, name="test2")
        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """ Tests that ingredients are returned only for auth-ed user """
        user = get_user_model().objects.create_user(
            email="test2@test.ru", password="password"
        )
        Ingredient.objects.create(user=user, name="test3")
        ingredient = Ingredient.objects.create(user=self.user, name="test4")
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)

    def test_create_ingredient_successful(self):
        """ test creation of a ingredient """
        payload = {"name": "ingredient"}
        self.client.post(INGREDIENT_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user, name=payload["name"]
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """ Test the creation of the Ingredient with invalid payload """
        payload = {"name": ""}
        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_ingredients_assigned_to_recipe(self):
        ingredient1 = Ingredient.objects.create(user=self.user, name="qwe")
        ingredient2 = Ingredient.objects.create(user=self.user, name="qwe2")
        recipe = Recipe.objects.create(
            user=self.user, title="asd", time_minutes=5, price=45.80
        )
        recipe.ingredients.add(ingredient1)
        res = self.client.get(INGREDIENT_URL, {"assigned_only": 1})
        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_ingredients_assigned_unique(self):
        ingredient1 = Ingredient.objects.create(user=self.user, name="qwe")
        ingredient2 = Ingredient.objects.create(user=self.user, name="qwe2")
        recipe = Recipe.objects.create(
            user=self.user, title="asd", time_minutes=5, price=45.80
        )
        recipe.ingredients.add(ingredient1)
        recipe2 = Recipe.objects.create(
            user=self.user, title="qwe", time_minutes=5, price=45.80
        )
        recipe2.ingredients.add(ingredient1)
        res = self.client.get(INGREDIENT_URL, {"assigned_only": 1})
        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)
        self.assertEqual(len(res.data), 1)
