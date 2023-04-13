from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .helpers_auth import get_jwt_token, send_signup_letter
from .permissions import IsAuthorOrModeratorOrAdminOrReadOnly
from .serializers import (
    ReviewSerializer,
    TokenRequestSerializer,
    UserSignupSerializer,
)
from reviews.models import Title

User = get_user_model()


@api_view(['POST'])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        username=serializer.data["username"],
        email=serializer.data["email"],
    )
    send_signup_letter(user)
    return Response()


@api_view(['POST'])
def jwt_token(request):
    serializer = TokenRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)  # <- проверяет confirmation_code
    user = User.objects.get(username=serializer.data["username"])
    user.role = User.Role.USER
    print(User.Role.USER)
    token = get_jwt_token(user)
    return Response({"token": token})


class ReviewViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы GET для всех отзывов, POST - создаёт новый отзыв,
    GET, PATCH, DELETE для одного отзыва по id отзыва."""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if self.request.user.reviews.filter(title=title):
            raise Exception('Можно написать только один отзыв')
        serializer.save(author=self.request.user, title=title)
