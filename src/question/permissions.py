from rest_framework.permissions import BasePermission, SAFE_METHODS


class QuestionOwnerOrSafeMethod(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'DELETE']:
            return obj.owner.user == request.user
        return False


class QuestionOwnerOrStaffOrSafeMethod(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.owner.user == request.user or request.user.is_staff is True
        return False
