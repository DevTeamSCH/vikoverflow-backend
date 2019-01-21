from rest_framework.permissions import BasePermission


# Permission class for the report viewset. All authenticated users are allowed to create reports, but only staff can
# access the other actions.
class ReportViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user:
            return False
        if request.method == "POST" and view.action == "create":
            return True
        return request.user.is_staff
