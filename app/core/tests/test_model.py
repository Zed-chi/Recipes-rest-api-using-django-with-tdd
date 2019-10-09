from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch


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

    def test_ingredient_str(self):
        ing = models.Ingredient.objects.create(
            user=sample_user(), name="tomato"
        )
        self.assertEqual(str(ing), ing.name)

    def test_recipe_as_str(self):
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="tomato with potato",
            time_minutes=5,
            price=5.00,
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch("uuid.uuid4")
    def test_recipe_imgfile_name_uuid(self, mock_uuid):
        uuid = "test"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, "myimage.jpg")
        exp_path = f"uploads/recipe/{uuid}.jpg"
        self.assertEqual(file_path, exp_path)
