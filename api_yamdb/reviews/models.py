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
