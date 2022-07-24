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
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

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

    def create_token_for_user(self):
        """
        Test generates token for valid credentials
        """

        user_details={
            'name':'Test Name',
            'password':'testpass',
            'email': 'test@example.com',
        }

        create_user(**user_details)
        payload={
            'email' : user_details['email'],
            'password':user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """
        Test returns error if credentials are invalid
        """

        create_user(email ='test@example.com', password = 'goodpass')
        payload = {
            'email':'test@example.com', 'password' : 'badpass' ,
        }

        res = self.client.post(TOKEN_URL , payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        payload = {
            'email' : 'test@example.com',
            'password' : '',
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test authentication is required for users
        """

        res = self.client.get(ME_URL)
        self.assertEqual(res.status, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """
    Test API requests that require authorization
    """

    def setUp(self):
        self.user = create_user(
            email ='test@nobella.com',
            name='Nobella Test',
            password='nobbytest12',
        )
        self.client = APIClient()
        #we do not need to properly authenticate a user for testing the API , this can be done using the below method
        self.client.force_authenticate(user = self.user)

    def retrieve_profile_success(self):
        """
        test for retrieving profile for logged in user 
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """
        Test POST is not allowed for the me api endpoint 
        """

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Test updating the user profile for the authenticated user 
         """

        payload = { 
            'name': 'Updated Name',
            'password': 'updated123',
        }

        res = self.client.patch(ME_URL , payload)
        #refresh the database to have the new data
        self.user.refresh_from_db()
        self.assertEqual(self.user.name , payload['name'])
        self.assertTrue(self.user.password, check_password(payload['password']))
        self.assertEqual(res.status_code , status.HTTP_200_OK)





