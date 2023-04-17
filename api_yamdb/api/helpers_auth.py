import binascii
import os

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def generate_confirmation_code() -> str:
    return binascii.hexlify(os.urandom(20)).decode()


def send_signup_letter(user: User) -> None:
    confirmation_code = generate_confirmation_code()
    user.set_password(confirmation_code)
    user.save()

    subject = "Ваш код подтверждения"
    body = confirmation_code
    email = EmailMessage(subject, body, to=[user.email])
    email.send()


def get_jwt_token(user: User) -> str:
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
