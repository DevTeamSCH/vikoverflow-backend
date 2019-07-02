from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Answer


class QuestionOwnerOrSafeMethodOrLoggedInCreate(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'DELETE']:
            return obj.owner.user == request.user
        return False


class AnswerOwnerCanModify(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'DELETE']:
            return obj.owner.user == request.user
        return False


class AnswerQuestionOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if Answer.objects.filter(id=obj.pk).exists():
            return Answer.objects.get(id=obj.pk).parent.owner.user == request.user
        return False


class QuestionOwnerOrStaffOrSafeMethod(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.owner.user == request.user or request.user.is_staff is True
        return False
