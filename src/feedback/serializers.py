from rest_framework import serializers

from . import models


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Ticket
        fields = ("url", "title", "text", "kind_of")
