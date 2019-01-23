from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
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

        if report.is_closed():
            raise ParseError()

        report.approved_by.add(request.user)

        ReportComment(
            text=_("Report approved"),
            owner=Profile.objects.get_or_create(user=request.user)[0],
            report=report
        ).save()

        if report.approved_by.count() >= 2:
            report.close()
            report.content_object.report_approved(report)

        report.save()
        return self.retrieve(request)

    @action(detail=True, methods=['post'], permission_classes=(IsAdminUser, ))
    def reject(self, request, pk=None):
        report = self.get_object()
        report.close()
        report.save()
        ReportComment(
            text=_("Report rejected"),
            owner=Profile.objects.get_or_create(user=request.user)[0],
            report=report
        ).save()
        return self.retrieve(request)

    @action(detail=True, methods=['post'], permission_classes=(IsSuperuser, ))
    def reopen(self, request, pk=None):
        report = self.get_object()
        report.reopen()
        report.save()
        ReportComment(
            text=_("Report reopened"),
            owner=Profile.objects.get_or_create(user=request.user)[0],
            report=report
        ).save()
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
