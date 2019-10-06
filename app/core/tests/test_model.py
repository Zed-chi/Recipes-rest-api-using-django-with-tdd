from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@tes.ru", password="secret"):
    """ Create a sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_creating_mode(self):
        """testing creation of user"""
        email = "test@test.com"
        password = "secret"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Tests the email is normalized """
        email = "test@TEST.com"
        password = "secret"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ testing that creating user with no email raises an error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "secret")

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            email="test@super.com", password="secret"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ test tag string"""
        tag = models.Tag.objects.create(user=sample_user(), name="qwe")
        self.assertEqual(str(tag), tag.name)
