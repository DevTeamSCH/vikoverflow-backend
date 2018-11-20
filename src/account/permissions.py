from rest_framework import permissions


class IsOwnProfileOrStaff(permissions.BasePermission):
    """
        Custom permission to only allow access to the owner or staff user
    """

    def has_object_permission(self, request, view, obj):

        if request.user:
            if request.user.is_staff:
                return True
            else:
                return obj.user == request.user
        else:
            return False


class ListStaffOnly(permissions.BasePermission):
    """
        Custom permission to only allow access to lists for staffs
    """

    def has_permission(self, request, view):
        return view.action != 'list' or (request.user and request.user.is_staff)
