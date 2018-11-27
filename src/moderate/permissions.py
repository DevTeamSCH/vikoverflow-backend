from rest_framework.permissions import BasePermission


class ReportListPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user:
            return False
        if request.method == "POST":
            return True
        return request.user.is_staff
