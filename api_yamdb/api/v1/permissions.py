from rest_framework import permissions
from reviews.constants import ADMIN, MODERATOR, SUPER_USER


class StaffOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            not request.user.is_anonymous
            and (
                request.user.role == ADMIN
                or request.user.role == SUPER_USER
                or request.user.is_staff
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            not request.user.is_anonymous
            and (
                request.user.role == ADMIN
                or request.user.role == SUPER_USER
                or request.user.is_staff
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return (
                request.user.role == ADMIN
                or request.user.role == SUPER_USER
                or request.user.is_staff
            )
        return False


class IsStaffOrModeratorOrAuthorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
            or request.user.role == MODERATOR
            or request.user.role == ADMIN
            or request.user.role == SUPER_USER
        )
