# flake8: noqa
"""
Tests for the tags API
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

def create_user(email = 'user@example.com', password = 'testpass123'):
    """
    Create and return a user .
    """
    return get_user_model().objects.create(email = email , password =password)

class  PublicTagsApiTests(TestCase):
    """
    Test unauthenticated API requests
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test auth is required for retrieving tags
        """
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code , status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTest(TestCase):
    """
    Test authenticated API request
    """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """
        Test for retrieving a likst of tags
        """
        Tag.objects.create(user = self.user ,name = 'Vegan')
        Tag.objects.create(user = self.user , name = 'Fruity')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags , many = True)

        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):

        """
        Test that listt oof tags is limited to authenticated user
        """
        user2 = create_user(email = 'example2.com' , password ='example12')
        Tag.objects.create(user = user2 , name = 'Fruity')
        tag = Tag.objects.create(user =self.user , name ='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],tag.name)
