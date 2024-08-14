from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Доступ администратора.
        Доступ разрешен если пользователь авторизирован
        и в группе администратор или суперпользователь.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(IsAdmin):
    """Доступ на изменение для администратора.
        Доступ разрешен если пользователь авторизирован
        и в группе администратор или суперпользователь.
    """

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            or request.method in permissions.SAFE_METHODS
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Доступ для автора, модератора или администратора.
        Доступ разрешен если пользователь авторизирован
        и автор или модератор или администратор или суперпользователь.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )