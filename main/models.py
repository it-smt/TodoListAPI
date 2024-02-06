from django.contrib.auth.models import User
from django.db import models


class Todo(models.Model):
    """Модель задачи."""

    class Status(models.TextChoices):
        """Возможные варианты для поля status."""
        DONE = "Готово", "Готово"
        NOT_DONE = "Не готово", "Не готово"

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.NOT_DONE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos', default=None)

    def __str__(self):
        return self.title
