# flake8: noqa

"""
Tests  for the user api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient 
from rest_framework import status

CREATE_USER_URL =  reverse("user:create")

def create_user(**params):
    """
    Create and return a new user .
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Test the public features of the user API. ie tests that don't require authentication ie registering a new user
    """
    def setUp(self):
        """
        creates an api client that can be used for testing
        """
        self.client = APIClient()

    def test_create_user_success(self):
        """
        Test creating a user is successful by posting the data to the API
        """

        payload ={
            'email': 'test@example.com',
            'password':'testpass123',
            'name':'Test Name',

        }
        #makes hhtp post request to the specified url with the payload
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        #retrieves objects from thhe database with email address passed in as payload , validate if the email was created
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_user_email_exists_error(self):
        """
        Test  error returned if user with email exists
        """
        payload ={
            'email': 'test@example.com',
            'password':'testpass123',
            'name':'Test Name',

        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_to_short_error(self):
        """
        Test an error is returned if password is less than 5 characters
        """
        payload ={
            'email': 'test@example.com',
            'password':'pw',
            'name':'Test Name',

        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST )
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)




