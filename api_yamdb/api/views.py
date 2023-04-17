from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from .filter import FilterTitles
from .helpers_auth import get_jwt_token, send_signup_letter
from .mixins import (
    ListCreateViewSet,
    RetrievUpdateViewSet,
    DestroyViewSet,
    AllViewSet,
)
from .permissions import (
    IsAdmin,
    IsAuthor,
    IsModerator,
    ReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTitleSerializer,
    ReviewSerializer,
    TitleSerializer,
    TokenRequestSerializer,
    UserCreateSerializer,
    UserMeUpdateSerializer,
    UserSignupSerializer,
    UserUpdateSerializer,
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


class UsersAdminViewSet(ListCreateViewSet):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)


class SingleUsersAdminViewSet(RetrievUpdateViewSet, DestroyViewSet):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = "username"
    lookup_value_regex = r"[\w.@+-]+"


class UserSelfViewSet(RetrievUpdateViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMeUpdateSerializer
    lookup_field = "_"
    lookup_value_regex = "me"

    def get_object(self):
        return self.request.user


class ReviewViewSet(AllViewSet):
    """Обрабатывает запросы GET для всех отзывов, POST - создаёт новый отзыв,
    GET, PATCH, DELETE для одного отзыва по id отзыва."""

    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        ReadOnly | IsAuthor | IsModerator | IsAdmin,
    )

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


class TitleViewSet(AllViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [ReadOnly | IsAdmin]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitles

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetTitleSerializer
        return TitleSerializer


class GenreViewSet(ListCreateViewSet, DestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdmin]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CategoryViewSet(ListCreateViewSet, DestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdmin]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CommentViewSet(AllViewSet):
    """Обрабатывает запросы GET для получения списка всех комментариев
    отзыва с id=review_id, POST создаёт новый комментарий,
    GET, PATCH, DELETE для одного комментария по id отзыва с id=review_id."""

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        ReadOnly | IsAuthor | IsModerator | IsAdmin,
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
