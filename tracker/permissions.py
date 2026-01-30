from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsAuthenticatedOrRegister(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.path == '/api/auth/register/':
            return True
        return request.user and request.user.is_authenticated
