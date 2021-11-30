# test models
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_success(self):
        """Test creating a user. Successful"""
        email = 'thisemail@gmail.com'
        password = '12345'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """TEst the email for a new user is normalized"""
        email = "test@THISISUPPER.com"
        user = get_user_model().objects.create_user(email, 'blabla123')

        self.assertAlmostEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test that a new user with invalid email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'asdafgg652354')

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'oneemail@another.com',
            'kumbaya123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
