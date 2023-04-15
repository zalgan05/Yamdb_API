from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


_username_field = serializers.RegexField(
    r"^[\w.@+-]+",
    min_length=4,
    max_length=150,
)


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


class UserSignupSerializer(serializers.ModelSerializer):
    username = _username_field
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "Нельзя выбрать \"me\" в качестве имени пользователя"
            )
        return value

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


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r"^[\w.@+-]+",
        min_length=4,
        max_length=150,
        required=False,
    )
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

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


class UserMeUpdateSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r"^[\w.@+-]+",
        min_length=4,
        max_length=150,
        required=False,
    )
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

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
        read_only_fields = ('role',)


class UserCreateSerializer(UserSignupSerializer):
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

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
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        exclude = ('title',)
        read_only_fields = ('author',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления/обновления/удаления произведения."""

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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "name",
            "slug",
        )
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "name",
            "slug",
        )
        model = Category


class GetTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для получения произведения/произведений."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ('review',)
        model = Comment
        read_only_fields = ('author',)
