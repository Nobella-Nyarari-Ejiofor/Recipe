# flake8: noqa
"""
Test for the ingredients api 
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from test_framework import status
from rest_framework.test import APIClient

from core.models import models

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
