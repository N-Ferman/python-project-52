from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Status


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            password="strong-pass-123",
        )
        self.status = Status.objects.create(name="Новый")

    def test_statuses_list_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("statuses"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Новый")

    def test_statuses_page_requires_login(self):
        response = self.client.get(reverse("statuses"))
        self.assertEqual(response.status_code, 302)

    def test_create_status(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("status_create"),
            {
                "name": "В работе",
            },
        )
        self.assertRedirects(response, reverse("statuses"))
        self.assertTrue(Status.objects.filter(name="В работе").exists())

    def test_update_status(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("status_update", args=[self.status.pk]),
            {
                "name": "На тестировании",
            },
        )
        self.assertRedirects(response, reverse("statuses"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "На тестировании")

    def test_delete_status(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("status_delete", args=[self.status.pk]),
        )
        self.assertRedirects(response, reverse("statuses"))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
