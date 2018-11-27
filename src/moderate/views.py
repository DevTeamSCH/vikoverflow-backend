from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from moderate.models import Report
from moderate.permissions import ReportListPermission
from moderate.serializers import ReportSerializer


class ReportViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (ReportListPermission, )

