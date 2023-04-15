from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title


UNAME_REGEX = r"^[\w.@+-]+"
UNAME_MIN_LEN = 4
UNAME_MAX_LEN = 150
EMAIL_MAX_LEN = 254
NAMES_MAX_LEN = 150

User = get_user_model()


class MixinUsernameRequired(serializers.Serializer):
    username = serializers.RegexField(
        UNAME_REGEX,
        min_length=UNAME_MIN_LEN,
        max_length=UNAME_MAX_LEN,
    )


class MixinUsernameOptional(serializers.Serializer):
    username = serializers.RegexField(
        UNAME_REGEX,
        min_length=UNAME_MIN_LEN,
        max_length=UNAME_MAX_LEN,
        required=False,
    )


class MixinEmail(serializers.Serializer):
    email = serializers.EmailField(max_length=EMAIL_MAX_LEN)


class MixinNames(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=NAMES_MAX_LEN, required=False
    )
    last_name = serializers.CharField(max_length=NAMES_MAX_LEN, required=False)


class TokenRequestSerializer(MixinUsernameRequired, serializers.Serializer):
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        uname = attrs["username"]
        ccode = attrs["confirmation_code"]
        user = get_object_or_404(User, username=uname)
        if not user.check_password(ccode):
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

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "Нельзя выбрать \"me\" в качестве имени пользователя"
            )  # в принципе, его и так нельзя будет выбрать, т.к. ограничение
            #    на длину не позволит
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
        read_only_fields = ('role',)


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
