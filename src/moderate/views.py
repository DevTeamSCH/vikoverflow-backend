from django.http import HttpResponseForbidden, HttpResponseBadRequest
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet

from account.models import Profile
from moderate.models import Report, ReportComment
from moderate.permissions import ReportViewSetPermission, IsSuperuser
from moderate.serializers import ReportSerializer


class ReportViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (ReportViewSetPermission,)

    @action(detail=True, methods=['post'], permission_classes=(IsAdminUser, ))
    def approve(self, request, pk=None):
        report = self.get_object()
        # TODO: Approve logic
        report.close()
        report.save()

        return self.retrieve(request)

    @action(detail=True, methods=['post'], permission_classes=(IsAdminUser, ))
    def reject(self, request, pk=None):
        report = self.get_object()
        report.close()
        report.save()
        return self.retrieve(request)

    @action(detail=True, methods=['post'], permission_classes=(IsSuperuser, ))
    def reopen(self, request, pk=None):
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        report = self.get_object()
        report.reopen()
        report.save()
        return self.retrieve(request)

    @action(detail=True, methods=['post'], permission_classes=(IsAdminUser, ))
    def comment(self, request, pk=None):
        report = self.get_object()
        comment_text = request.data.get('comment')
        if comment_text is None:
            return HttpResponseBadRequest()
        comment = ReportComment(
            text=comment_text,
            owner=Profile.objects.get_or_create(user=request.user)[0],
            report=report
        )
        comment.save()
        return self.retrieve(request)
