from rest_framework.viewsets import ModelViewSet

from moderate.models import Report
from moderate.serializers import ReportSerializer, ReportCreateSerializer


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReportCreateSerializer
        else:
            return ReportSerializer

