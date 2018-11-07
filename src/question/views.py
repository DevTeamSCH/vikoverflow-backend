from taggit.models import Tag
from rest_framework import mixins, viewsets, permissions
from . import serializers
from common.mixins import RelativeURLFieldMixin



class TagViewSet(
    RelativeURLFieldMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.TagSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Tag.objects.all()
