from django.test import TestCase


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