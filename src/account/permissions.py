from rest_framework import permissions


class IsSafeMethodOrIsOwnOrIsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'PUT':
            return request.user
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT':
            return request.user.is_superuser or obj.user == request.user
        return request.method in permissions.SAFE_METHODS
