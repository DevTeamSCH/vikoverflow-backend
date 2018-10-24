from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions

from common.mixins import RelativeURLFieldMixin
from . import models
from . import serializers


class TicketViewSet(
    RelativeURLFieldMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Ticket.objects.all()
    serializer_class = serializers.TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def check_permissions(self, request):
        # Allow GET when ticket was posted
        if request.method in ["DELETE", "GET"] and request.POST.get('pk') is None:
            self.permission_classes.append(permissions.IsAdminUser)
        super().check_permissions(request)
