from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .helpers_auth import check_confirmation_code
from .mixins.serializers import (
    MixinEmail,
    MixinNames,
    MixinUsernameOptional,
    MixinUsernameRequired,
)
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class TokenRequestSerializer(MixinUsernameRequired, serializers.Serializer):
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        uname = attrs["username"]
        ccode = attrs["confirmation_code"]
        user = get_object_or_404(User, username=uname)

        if not check_confirmation_code(user, ccode):
            raise serializers.ValidationError("Неправильный код подтверждения")
        return super().validate(attrs)


class BaseUserModelSerializer(
    MixinEmail, MixinNames, serializers.ModelSerializer
):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        ]


class UserSignupSerializer(
    MixinUsernameRequired, MixinEmail, serializers.ModelSerializer
):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]

    def validate(self, attrs):
        uname = attrs["username"]
        email = attrs["email"]
        uname_exists = (
            User.objects.filter(username=uname).exclude(email=email).exists()
        )
        email_exists = (
            User.objects.filter(email=email).exclude(username=uname).exists()
        )
        if uname_exists or email_exists:
            raise serializers.ValidationError(
                "Данная комбинация (username, email) конфликтует с "
                "существующей учётной записью"
            )
        return super().validate(attrs)


class UserUpdateSerializer(MixinUsernameOptional, BaseUserModelSerializer):
    pass


class UserMeUpdateSerializer(
    MixinUsernameOptional, serializers.ModelSerializer
):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        ]
        read_only_fields = ["role"]


class UserCreateSerializer(MixinNames, UserSignupSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """Преобразовывает объекты модели Review"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Review
        exclude = ["title"]
        read_only_fields = ["author"]


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления/обновления/удаления произведения."""

    genre = SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    rating = serializers.FloatField(required=False)

    class Meta:
        fields = [
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        ]  # порядок вывода, как в redoc
        model = Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "name",
            "slug",
        ]
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "name",
            "slug",
        ]
        model = Category


class GetTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для получения произведения/произведений."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField(required=False)

    class Meta:
        fields = [
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        ]  # порядок вывода, как в redoc
        model = Title
        read_only_field = ['rating']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        exclude = ["review"]
        model = Comment
        read_only_fields = ["author"]
