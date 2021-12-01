from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')  # url of the authenticated user


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests creation an unauthenticated user"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload successfull"""
        payload = {
            'email': 'kumbayah@gmail.com',
            'password': 'testthis',
            'name': 'some name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # confirms the request created a user
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # verify that the user was trully created
        user = get_user_model().objects.get(**res.data)
        # test that the password is correct
        self.assertTrue(user.check_password(payload['password']))
        # confirms that the password is not present in the response
        # as it would be a potential security threat
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating an already existing user"""
        payload = {
            'email': 'kumbayah@gmail.com',
            'password': 'testthis',
            'name': 'bambi',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        """Tests that the pass must be > 5 chars"""
        payload = {
            'email': 'kumbayah@gmail.com',
            'password': 'te',
            'name': 'rambo',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token(self):
        """test that a token is created for a user"""
        payload = {
            'email': 'kumbayahmylord@gmail.com',
            'password': 'teainabasket',
            'name': 'rambo2',
        }
        create_user(**payload)
        # remember that this doesn't create a user,
        # only checks the token for one
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_invalid_token(self):
        """Test that a token is not created for invalid credentials"""
        payload1 = {
            'email': 'kumbayahmylord@gmail.com',
            'password': 'teainabasket',
            'name': 'rambo2',
        }
        create_user(**payload1)
        payload2 = {
            'email': 'kumbayahmylord@gmail.com',
            'password': 'thisisthewrongpassword',
            'name': 'rambo2',
        }
        # tries to creata a token with the wrong password
        res = self.client.post(TOKEN_URL, payload2)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        # same as invalid token, but without creating the user
        payload = {
            'email': 'kumbayahmylord@gmail.com',
            'password': 'teainabasket',
            'name': 'rambo2',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_data(self):
        """Tests tjat token is not created if password is invalid"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test api requests that require authentication"""
    def setUp(self):
        self.user = create_user(
            email='test@gmail.com',
            password='testpass',
            name='rambo'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_authorized(self):
        """test retrieving profile for logged user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_not_allowed(self):
        """test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'name': 'new_name',
            'email': 'test@gmail.com',
            'password': 'pass123'
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
