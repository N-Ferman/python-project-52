from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class UserCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="tester",
            password="strong-pass-123",
            first_name="Test",
            last_name="User",
        )

    def test_create_user(self):
        response = self.client.post(
            reverse("user_create"),
            {
                "first_name": "New",
                "last_name": "User",
                "username": "newuser",
                "password1": "complex-pass-123",
                "password2": "complex-pass-123",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_update_self(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("user_update", args=[self.user.pk]),
            {
                "first_name": "Updated",
                "last_name": "User",
                "username": "tester",
            },
        )
        self.assertRedirects(response, reverse("users"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_delete_self(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("user_delete", args=[self.user.pk]))
        self.assertRedirects(response, reverse("users"))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())


# Create your tests here.
