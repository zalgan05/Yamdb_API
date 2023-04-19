from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


def send_signup_letter(user: User) -> None:
    confirmation_code = token_generator.make_token(user)

    subject = "Ваш код подтверждения"
    body = confirmation_code
    email = EmailMessage(subject, body, to=[user.email])
    email.send()


def check_confirmation_code(user: User, confirmation_code: str) -> bool:
    if user.is_superuser:
        return True
    return token_generator.check_token(user, confirmation_code)


def get_jwt_token(user: User) -> str:
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
