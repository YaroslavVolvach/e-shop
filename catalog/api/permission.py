from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if method in permissions.SAFE_METHODS:
            return True

        if method == 'PUT':
            return obj.user == user

        if method == 'POST':
            return user.is_active

        return (obj.user == user) or user.is_staff


class AdminOrReadonlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff
