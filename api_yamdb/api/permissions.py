from rest_framework import permissions

from reviews.constants import ROLES


class IsAuthorAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, дающее возможность редактирования только владельцам объекта.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if (request.method in permissions.SAFE_METHODS or
                    request.user.role == ROLES.moderator or
                    request.user.role == ROLES.admin):
                return True
        return obj.author == request.user
