from rest_framework import viewsets
from rest_framework import mixins

from . import models
from . import serializers

class CommentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
