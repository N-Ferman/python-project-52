from django.contrib.auth.models import User
from django.db import models

from task_labels_app.models import Label
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='Статус',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
        verbose_name='Автор',
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executed_tasks',
        verbose_name='Исполнитель',
        blank=True,
        null=True,
    )
    labels = models.ManyToManyField(
        Label,
        related_name='tasks',
        blank=True,
        verbose_name='Метки',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name