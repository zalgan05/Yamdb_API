from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helpers_auth import send_signup_letter
from .serializers import UserSerializer

User = get_user_model()


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        username=serializer.data["username"],
        email=serializer.data["email"],
    )
    send_signup_letter(user)
    return Response()
