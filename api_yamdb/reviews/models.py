import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


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

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр произведения."""

    name = models.CharField(max_length=256, verbose_name="Название")
    slug = models.SlugField(unique=True, max_length=50, verbose_name="Слаг")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение."""

    name = models.CharField(max_length=256, verbose_name="Название")
    year = models.IntegerField(
        validators=[
            MaxValueValidator(
                limit_value=dt.datetime.now().year,
                message="Год выпуска не может быть больше текущего.",
            ),
        ],
        verbose_name="Год выпуска",
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    genre = models.ManyToManyField(Genre, verbose_name="Жанр")
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
    )

    class Meta:
        default_related_name = "titles"
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ["name"]

    @property
    def rating(self):
        reviews = self.reviews
        if not reviews:
            return None
        return reviews.aggregate(Avg("score"))["score__avg"]

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.IntegerField(
        "Оценка произведения",
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ],
    )
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)  # Добавлено для корректной пагинации
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],  # Один пользователь - один отзыв
                name="unique_review",
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)
