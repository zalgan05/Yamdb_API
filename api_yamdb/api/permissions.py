from rest_framework import permissions

from reviews.models import User


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAnyone(permissions.AllowAny):
    """
    IsAnyone = IsAnonimus or IsUser or IsModerator or IsAdmin
    """

    pass


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.USER
        )


class IsAccessingOneself(permissions.IsAuthenticated):
    """Пользователь может иметь доступ только к своей собственной записи
    пользователя"""

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, User):
            return False
        return request.user.username == obj.username


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.MODERATOR
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == User.Role.ADMIN
        )


# Действие с объектом разрешены только для автора объекта, администратора и
#  модератора
"""IsAuthorOrModeratorOrAdminOrReadOnly = (
    ReadOnly | IsAuthor | IsModerator | IsAdmin
)"""


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Действие с объектом разрешены только для автора объекта,
    администратора и модератора"""

    message = 'Вам недоступно это действие'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.role == User.Role.ADMIN
            or request.user.role == User.Role.MODERATOR
        )
