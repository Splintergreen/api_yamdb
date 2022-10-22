from django.contrib.auth.models import AnonymousUser

from rest_framework import permissions

from reviews.constants import MODERATOR, ADMIN, SUPER_USER


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, дающее возможность редактирования только владельцам объекта.
    """

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS or
                request.user.role == MODERATOR or
                request.user.role == ADMIN or
                request.user.role == SUPER_USER):
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, дающее возможность редактирования только админам, чтение-всем.
    """

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS or
                not request.user.is_anonymous and (
                        request.user.role == ADMIN or
                        request.user.role == SUPER_USER
                )
        )
