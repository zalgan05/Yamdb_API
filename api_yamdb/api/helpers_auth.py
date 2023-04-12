import binascii
import os

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

User = get_user_model()


def generate_confirmation_code():
    return binascii.hexlify(os.urandom(20)).decode()


def send_signup_letter(user: User):
    confirmation_code = generate_confirmation_code()
    user.set_password(confirmation_code)
    user.save()

    subject = "Ваш код подтверждения"
    body = confirmation_code
    email = EmailMessage(subject, body, to=[user.email])
    email.send()
