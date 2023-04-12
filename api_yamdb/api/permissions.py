from rest_framework import permissions
from reviews.models import User


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Действие с объектом разрешены только для автора объекта,
    администратора и модератора."""

    message = 'Вам недоступно это действие'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user or request.user.role == User.Role.ADMIN
            or request.user.role == User.Role.MODERATOR
        )
