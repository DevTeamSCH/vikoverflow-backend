from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse

from . import models
from . import serializers
from account.models import Profile


class AnswerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer


class QuestionViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer

    def put(self, request, pk, *args, **kwargs):
        question = get_object_or_404(models.Question, pk=pk)
        user = request.user
        user_profile = Profile.objects.get(user=user)
        upvoters = question.votes.upvoters
        downvoters = question.votes.downvoters
        bad_request = HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        try:
            vote = request.data['user_vote']
        except KeyError:
            return bad_request

        if vote == 'up':
            if upvoters.filter(user=user).count() > 0:
                upvoters.remove(user_profile)
            elif downvoters.filter(user=user).count() > 0:
                downvoters.remove(user_profile)
                upvoters.add(user_profile)
            else:
                upvoters.add(user_profile)
        elif vote == 'down':
            if downvoters.filter(user=user).count() > 0:
                downvoters.remove(user_profile)
            elif upvoters.filter(user=user).count() > 0:
                upvoters.remove(user_profile)
                downvoters.add(user_profile)
            else:
                downvoters.add(user_profile)
        else:
            return bad_request

        return HttpResponse(status=status.HTTP_200_OK)
