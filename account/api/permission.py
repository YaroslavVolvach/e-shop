from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if method in permissions.SAFE_METHODS:
            return True

        return obj == user


class ChangePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_staff:
            return False
        return (not obj.is_staff) or user.is_superuser
