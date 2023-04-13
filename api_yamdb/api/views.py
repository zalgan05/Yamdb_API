from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Category, Genre, Title

from .mixins import ListCreateDestroyViewSet
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = None  # добавить
    pagination_class = LimitOffsetPagination  # из тестов посмотреть какая
    # пагинация
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category", "genre", "name", "year")


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = None  # добавить
    pagination_class = LimitOffsetPagination  # из тестов посмотреть какая
    # пагинация
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = None  # добавить
    pagination_class = LimitOffsetPagination  # из тестов посмотреть какая
    # пагинация
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
