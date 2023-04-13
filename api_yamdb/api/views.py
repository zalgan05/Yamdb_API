from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Title

from .permissions import IsAuthorOrModeratorOrAdminOrReadOnly
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы GET для всех отзывов, POST - создаёт новый отзыв,
    GET, PATCH, DELETE для одного отзыва по id отзыва."""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdminOrReadOnly
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
