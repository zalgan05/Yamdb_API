from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Genre, Title, Category
from .mixins import ListCreateDestroyViewSet
from .serializers import (TitleSerializer, GenreSerializer, CategorySerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = None  # добавить
    pagination_class = LimitOffsetPagination  # из тестов посмотреть какая
    # пагинация


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
