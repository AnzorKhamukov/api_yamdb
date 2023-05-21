from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Доступ только администраторам."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ для чтения всем, на изменение - администраторам."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))
