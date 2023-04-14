from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .helpers_auth import get_jwt_token, send_signup_letter
from .mixins import ListCreateDestroyViewSet
from .permissions import (
    IsAdmin,
    IsAnyone,
    IsAuthor,
    IsAuthorOrModeratorOrAdminOrReadOnly,
    IsModerator,
    IsUser,
    ReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TokenRequestSerializer,
    UserCreateSerializer,
    UserSignupSerializer,
)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        username=serializer.data["username"],
        email=serializer.data["email"],
    )
    send_signup_letter(user)
    return Response(request.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_token(request):
    serializer = TokenRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)  # <- проверяет confirmation_code
    user = User.objects.get(username=serializer.data["username"])
    token = get_jwt_token(user)
    return Response({"token": token})


class UsersAdminViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы GET для всех отзывов, POST - создаёт новый отзыв,
    GET, PATCH, DELETE для одного отзыва по id отзыва."""

    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )
    http_method_names = ['get', 'post', 'patch', 'delete']  # Убран метод PUT

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if self.request.user.reviews.filter(title=title):
            raise serializers.ValidationError(
                'Можно написать только один отзыв'
            )
        serializer.save(author=self.request.user, title=title)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [ReadOnly | IsAdmin]
    pagination_class = LimitOffsetPagination  # из тестов посмотреть какая
    # пагинация
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category", "genre", "name", "year")


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdmin]
    pagination_class = LimitOffsetPagination  # из тестов посмотреть какая
    # пагинация
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdmin]
    pagination_class = LimitOffsetPagination  # из тестов посмотреть какая
    # пагинация
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class CommentViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы GET для получения списка всех комментариев
    отзыва с id=review_id, POST создаёт новый комментарий,
    GET, PATCH, DELETE для одного комментария по id отзыва с id=review_id."""

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()
