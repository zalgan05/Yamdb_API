from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator

import datetime as dt



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


class Category(models.Model):
    """Категория произведения."""
    name = models.CharField(max_length=256, verbose_name="Название")
    slug = models.SlugField(unique=True, max_length=50, verbose_name="Слаг")

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр произведения."""
    name = models.CharField(max_length=256, verbose_name="Название")
    slug = models.SlugField(unique=True, max_length=50, verbose_name="Слаг")

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение."""
    name = models.CharField(max_length=256, verbose_name="Название")
    year = models.IntegerField(validators=[MaxValueValidator(
        limit_value=dt.datetime.now().year,
        message="Год выпуска не может быть больше текущего."), ],
                               verbose_name="Год выпуска")
    description = models.TextField(blank=True, verbose_name="Описание")
    genre = models.ManyToManyField(Genre, verbose_name="Жанр")
    category = models.ForeignKey(
        Category, to_field="slug", null=True,
        on_delete=models.SET_NULL, verbose_name="Категория")

    class Meta:
        default_related_name = "titles"

    @property
    def rating(self):
        reviews = self.reviews  # получение отзывов по related name - reviews
        if not reviews:
            return None
        return reviews.aggregate(Avg("score"))

    def __str__(self):
        return self.name
