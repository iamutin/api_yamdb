from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated and request.user.is_admin
        )


class AuthorModeratorAdminOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return request.method in permissions.SAFE_METHODS or (
                user.is_authenticated and
                (obj.author == user or user.is_admin or user.is_moderator)
        )
