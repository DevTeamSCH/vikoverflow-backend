from django.http import HttpResponseForbidden
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from moderate.models import Report
from moderate.permissions import ReportListPermission
from moderate.serializers import ReportSerializer


class ReportViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (ReportListPermission, )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        report = self.get_object()
        # TODO: Approve logic
        report.close()
        report.save()

        return self.retrieve(request)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        report = self.get_object()
        report.close()
        report.save()
        return self.retrieve(request)

    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        report = self.get_object()
        report.reopen()
        report.save()
        return self.retrieve(request)
