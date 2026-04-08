from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from .models import Task

class TaskCRUDTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='author',
            password='strong-pass-123',
        )
        self.executor = User.objects.create_user(
            username='executor',
            password='strong-pass-123',
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='strong-pass-123',
        )
        self.status = Status.objects.create(name='Новый')
        self.label = Label.objects.create(name='bug')

        self.task = Task.objects.create(
            name='Первая задача',
            description='Описание задачи',
            status=self.status,
            author=self.author,
            executor=self.executor,
        )
        self.task.labels.add(self.label)

    
    def test_tasks_page_requires_login(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)

    def test_tasks_list_for_logged_user(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Первая задача')
        
    def test_show_task(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('task_show', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Описание задачи')
        
    def test_create_task(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('task_create'), {
            'name': 'Новая задача',
            'description': 'Новый текст',
            'status': self.status.pk,
            'executor': self.executor.pk,
            'labels': [self.label.pk],
        })
        self.assertRedirects(response, reverse('tasks'))
        created = Task.objects.get(name='Новая задача')
        self.assertEqual(created.author, self.author)
        self.assertEqual(created.executor, self.executor)
        self.assertEqual(created.status, self.status)
        self.assertTrue(created.labels.filter(pk=self.label.pk).exists())

    def test_update_task(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('task_update', args=[self.task.pk]), {
            'name': 'Обновленная задача',
            'description': 'Новое описание',
            'status': self.status.pk,
            'executor': self.executor.pk,
            'labels': [self.label.pk],
        })
        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Обновленная задача')

    def test_delete_task_by_author(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())  

    def test_delete_task_by_not_author_forbidden(self):
        self.client.force_login(self.other_user)
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())