from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse

from . import models
from . import serializers
from account.models import Profile


def handle_vote(abstract_comment, request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    upvoters = abstract_comment.votes.upvoters
    downvoters = abstract_comment.votes.downvoters
    bad_request = HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    try:
        vote = request.data['user_vote']
    except KeyError:
        return bad_request
    if vote == 'up':
        if downvoters.filter(user=user).count() > 0:
            downvoters.remove(user_profile)
            upvoters.add(user_profile)
        else:
            upvoters.add(user_profile)
    elif vote == 'down':
        if upvoters.filter(user=user).count() > 0:
            upvoters.remove(user_profile)
            downvoters.add(user_profile)
        else:
            downvoters.add(user_profile)
    elif vote == 'none':
        if upvoters.filter(user=user).count() > 0:
            upvoters.remove(user_profile)
        elif downvoters.filter(user=user).count() > 0:
            downvoters.remove(user_profile)
    else:
        return bad_request
    return HttpResponse(status=status.HTTP_200_OK)


class AnswerVoteViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer

    def update(self, request, pk):
        answer = get_object_or_404(models.Answer, pk=pk)
        return handle_vote(answer, request)


class CommentVoteViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def update(self, request, pk):
        answer = get_object_or_404(models.Comment, pk=pk)
        return handle_vote(answer, request)


class QuestionViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer

    def update(self, request, pk):
        question = get_object_or_404(models.Question, pk=pk)
        return handle_vote(question, request)
