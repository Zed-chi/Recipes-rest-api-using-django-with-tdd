from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_creating_mode(self):
        """testing creation of user"""
        email = "test@test.com"
        password = "secret"
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
