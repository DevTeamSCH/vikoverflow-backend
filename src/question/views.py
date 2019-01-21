from rest_framework import viewsets
from rest_framework import mixins

from . import models
from . import serializers


class QuestionViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
