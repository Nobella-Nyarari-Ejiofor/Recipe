# flake8: noqa
"""
Test for the ingredients api 
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

def create_user(    email = 'ingredient@example.com' , password = 'example12'):
    """
    create and return user 
    """


    return get_user_model().objects.create_user(email = email , password = password)


class PublicIngredientsAPITests(TestCase):
    """
    Test unauthenticated API's
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test auth is required for retrieving ingredient
        """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code , status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsAPITests(TestCase):
    """
    Test Authorized API requests
    """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """
        Test retrieving a list of ingredients
        """
        Ingredient.objects.create(user = self.user , name = 'Tomato')
        Ingredient.objects.create(user = self.user, name = 'Onion')

        res = self.client.get(INGREDIENTS_URL)

        ingredients =  Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many = True)

        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_ingredients_limited_to_user(self):
        """
        Test list of ingredients is limited to the user
        """
        user2 = create_user(email = "example2@me.com")
        Ingredient.objects.create(user = user2 , name ='Salt')

        ingredient =Ingredient.objects.create(user = self.user , name = 'Pepper')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

        


