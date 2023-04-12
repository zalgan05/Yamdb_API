from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "user"
        MODERATOR = "moderator"
        ADMIN = "admin"

    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.CharField(
        "Пользовательская роль",
        max_length=64,
        choices=Role.choices,
        default=Role.USER,
    )


class Review(models.Model):
    text = models.TextField(),
    title = models.ForeignKey(
        Title,  # Проверить при добавлении модели Title
        on_delete=models.CASCADE,
        related_name='reviews',
    ),
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    ),
    score = models.IntegerField(
        'Оценка произведения',
        min_value=1,
        max_value=10
    ),
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)
