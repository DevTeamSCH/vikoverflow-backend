from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import action
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
    elif vote == 'down':
        if upvoters.filter(user=user).count() > 0:
            upvoters.remove(user_profile)
        downvoters.add(user_profile)
    elif vote == 'none':
        if upvoters.filter(user=user).count() > 0:
            upvoters.remove(user_profile)
        elif downvoters.filter(user=user).count() > 0:
            downvoters.remove(user_profile)
    else:
        return bad_request
    return HttpResponse(status=status.HTTP_200_OK)


class Votable(viewsets.GenericViewSet):
    model = None


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = self.model.objects.all()


    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def vote(self, request, pk):
        abstract_comment = get_object_or_404(self.model, pk=pk)
        return handle_vote(abstract_comment, request)


class AnswerViewSet(Votable):
    model = models.Answer
    serializer_class = serializers.AnswerSerializer


class CommentViewSet(Votable):
    model = models.Comment
    serializer_class = serializers.CommentSerializer


class QuestionViewSet(
    mixins.RetrieveModelMixin,
    Votable
):
    model = models.Question
    serializer_class = serializers.QuestionSerializer
