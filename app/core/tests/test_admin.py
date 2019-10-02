from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="secret"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@mail.com",
            password="secret",
            name="some_name"
        )

    def test_users_listed(self):
        """test that users are listed on the page"""
        url = reverse("admin:core_usermodel_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        """ tests that the user edit page works """
        url = reverse("admin:core_usermodel_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
