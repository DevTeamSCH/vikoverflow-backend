from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions

from common.mixins import RelativeURLFieldMixin
from .permissions import IsAdminOrCreate
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
    permission_classes = (permissions.IsAuthenticated, IsAdminOrCreate)
