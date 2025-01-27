from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to users with the 'admin' role.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsUser(permissions.BasePermission):
    """
    Allows access only to users with the 'user' role.
    """
    def has_permission(self, request, view):
        return request.user.role == 'user'