from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.RegexField(
        r"^[\w.@+-]+",
        min_length=4,
        max_length=150,
    )

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
