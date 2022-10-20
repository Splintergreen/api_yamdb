from rest_framework import permissions

from reviews.constants import ROLES


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, дающее возможность редактирования только владельцам объекта.
    """

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS or
                request.user.role == ROLES.MODERATOR or
                request.user.role == ROLES.ADMIN or
                request.user.role == ROLES.SUPER_USER):
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, дающее возможность редактирования только админам, чтение-всем.
    """

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS or
                request.user.role == ROLES.ADMIN or
                request.user.role == ROLES.SUPER_USER
        )
