from rest_framework import serializers

UNAME_REGEX = r"^[\w.@+-]+"
UNAME_MIN_LEN = 4
UNAME_MAX_LEN = 150
EMAIL_MAX_LEN = 254
NAMES_MAX_LEN = 150


class MixinUsernameRequired(serializers.Serializer):
    username = serializers.RegexField(
        UNAME_REGEX,
        min_length=UNAME_MIN_LEN,
        max_length=UNAME_MAX_LEN,
    )

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                'Нельзя выбрать "me" в качестве имени пользователя'
            )  # в принципе, его и так нельзя будет выбрать, т.к. ограничение
            #    на длину не позволит
        return value


class MixinUsernameOptional(MixinUsernameRequired):
    username = serializers.RegexField(
        UNAME_REGEX,
        min_length=UNAME_MIN_LEN,
        max_length=UNAME_MAX_LEN,
        required=False,
    )


class MixinEmail(serializers.Serializer):
    email = serializers.EmailField(max_length=EMAIL_MAX_LEN)


class MixinNames(serializers.Serializer):
    """first_name, last_name fields"""

    first_name = serializers.CharField(
        max_length=NAMES_MAX_LEN, required=False
    )
    last_name = serializers.CharField(max_length=NAMES_MAX_LEN, required=False)
