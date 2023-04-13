from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Review, Title

User = get_user_model()

_username_field = serializers.RegexField(
    r"^[\w.@+-]+",
    min_length=4,
    max_length=150,
)


class UserSignupSerializer(serializers.Serializer):
    username = _username_field
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "Нельзя выбрать \"me\" в качестве имени пользователя"
            )
        return value

    def validate(self, attrs):
        uname = attrs["username"]
        email = attrs["email"]
        if (
            User.objects.filter(username=uname).exclude(email=email).exists()
            or User.objects.filter(email=email)
            .exclude(username=uname)
            .exists()
        ):
            raise serializers.ValidationError(
                "Данная комбинация (username, email) конфликтует с "
                "существующей учётной записью"
            )
        return super().validate(attrs)


class TokenRequestSerializer(serializers.Serializer):
    username = _username_field
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        uname = attrs["username"]
        ccode = attrs["confirmation_code"]
        user = get_object_or_404(User, username=uname)
        if not user.check_password(ccode):
            raise serializers.ValidationError("Неправильный код подтверждения")
        return super().validate(attrs)


class ReviewSerializer(serializers.ModelSerializer):
    """Преобразовывает объекты модели Review"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = (
            'author',
            'title',
        )


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )  # порядок вывода, как в redoc
        model = Title


class GenreSerializer:
    class Meta:
        fields = "__all__"
        model = Genre


class CategorySerializer:
    class Meta:
        fields = "__all__"
        model = Category

