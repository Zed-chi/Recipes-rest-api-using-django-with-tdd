from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag, Recipe
from recipe.serializers import TagSerializer


TAGS_URL = reverse("recipe:tag-list")


class PublicTagsApiTests(TestCase):
    """ Tests public tags api """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Tests that login is required to operate with tag api """
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """ Test tags api with authorized user """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.ru", password="password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """ Tests gitting tags list """
        Tag.objects.create(user=self.user, name="test")
        Tag.objects.create(user=self.user, name="test2")
        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """ Tests that tags are returned only for auth-ed user """
        user = get_user_model().objects.create_user(
            email="test2@test.ru", password="password"
        )
        Tag.objects.create(user=user, name="test3")
        tag = Tag.objects.create(user=self.user, name="test4")
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)

    def test_create_tag_successful(self):
        """ test creation of a tag """
        payload = {"name": "testtag"}
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user, name=payload["name"]
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """ Test the creation of the tag with invalid payload """
        payload = {"name": ""}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_assigned_to_recipe(self):
        tag1 = Tag.objects.create(user=self.user, name="qwe")
        tag2 = Tag.objects.create(user=self.user, name="qwe2")
        recipe = Recipe.objects.create(
            user=self.user, title="asd", time_minutes=5, price=45.80
        )
        recipe.tags.add(tag1)
        res = self.client.get(TAGS_URL, {"assigned_only": 1})
        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_tags_assigned_unique(self):
        tag1 = Tag.objects.create(user=self.user, name="qwe")
        Tag.objects.create(user=self.user, name="qwe2")
        recipe = Recipe.objects.create(
            user=self.user, title="asd", time_minutes=5, price=45.80
        )
        recipe.tags.add(tag1)
        recipe2 = Recipe.objects.create(
            user=self.user, title="qwe", time_minutes=5, price=45.80
        )
        recipe2.tags.add(tag1)
        res = self.client.get(TAGS_URL, {"assigned_only": 1})
        self.assertEqual(len(res.data), 1)
