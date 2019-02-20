from rest_framework.permissions import BasePermission


class ReportViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == "list" or view.action == "retrieve":
            return request.user.is_staff
        return True


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
