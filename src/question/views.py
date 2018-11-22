from rest_framework import viewsets
from rest_framework import mixins

from . import models
from . import serializers


class AnswerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer


class QuestionViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
