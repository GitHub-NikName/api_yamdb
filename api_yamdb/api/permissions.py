from rest_framework import permissions


class RolePermissions(permissions.BasePermission):
    allowed_roles = ('user', 'moderator', 'admin')

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )


# class IsUser(RolePermissions):
#     allowed_roles = ('user', )
#
#
# class IsModerator(RolePermissions):
#     allowed_roles = ('moderator', )


class IsAdmin(RolePermissions):
    allowed_roles = ('admin', )

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.role in self.allowed_roles
            or request.user.is_staff
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.role in self.allowed_roles
                or request.user.is_staff
            )
        )


class IsOwnerModerAdminOrReadOnly(permissions.BasePermission):
    """ + для автора, модератора, админа или только чтение,
    + пост метод для аторизированных пользователей"""

    allowed_roles = ('moderator', 'admin')

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )
