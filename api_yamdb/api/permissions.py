from rest_framework import permissions

from reviews.models import User


class BaseConsecutivePermission(permissions.BasePermission):
    """Последовательно применяет к `has_object_permission()` те же правила, что
      были применены в `has_permission()`.
      От слова "сonsecutive" - "последовательный".
    Не подходит для классов, которые выдают разрешения,
      основываясь на полях `obj`."""

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ReadOnly(BaseConsecutivePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user


class IsModerator(BaseConsecutivePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.MODERATOR
        )


class IsAdmin(BaseConsecutivePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == User.Role.ADMIN
        )
