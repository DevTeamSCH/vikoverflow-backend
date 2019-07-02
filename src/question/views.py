from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from account.models import Profile
from common.models import Votes
from . import models
from . import serializers
from .permissions import (
    QuestionOwnerOrSafeMethodOrLoggedInCreate,
    AnswerOwnerCanModify,
    AnswerQuestionOwner,
    QuestionOwnerOrStaffOrSafeMethod
)


def handle_vote(abstract_comment, request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    upvoters = abstract_comment.votes.upvoters
    downvoters = abstract_comment.votes.downvoters
    bad_request = HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    try:
        vote = request.data["user_vote"]
    except KeyError:
        return bad_request
    if vote == "up":
        if downvoters.filter(user=user).count() > 0:
            downvoters.remove(user_profile)
        upvoters.add(user_profile)
    elif vote == "down":
        if upvoters.filter(user=user).count() > 0:
            upvoters.remove(user_profile)
        downvoters.add(user_profile)
    elif vote == "none":
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

    @action(
        detail=True, methods=["put"], permission_classes=[permissions.IsAuthenticated]
    )
    def vote(self, request, pk):
        abstract_comment = get_object_or_404(self.model, pk=pk)
        return handle_vote(abstract_comment, request)


class AnswerViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, Votable):
    model = models.Answer
    serializer_class = serializers.AnswerSerializer
    permission_classes = [AnswerOwnerCanModify]

    def update(self, request, *args, **kwargs):
        return super(AnswerViewSet, self).update(request, *args, **kwargs, partial=True)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def comments(self, request, pk):
        answer = get_object_or_404(self.model, pk=pk)
        user_profile = request.user.profile
        try:
            text = request.data['text']
            show_username = request.data['show_username']
        except KeyError:
            return HttpResponseBadRequest('Text and show_username field cannot be empty!')
        comment = models.Comment.objects.create(
            text=text,
            show_username=show_username,
            votes=Votes.objects.create(),
            parent_answer=answer,
            owner=user_profile
        )
        serializer = serializers.CommentSerializer(comment)
        return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["put"], permission_classes=[AnswerQuestionOwner])
    def accept(self, request, pk):
        try:
            accepted = request.data["accepted"]
        except KeyError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        answer = self.get_object()
        answer.is_accepted = accepted
        answer.save()
        serializer = serializers.AnswerSerializer(answer)
        return HttpResponse(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


class CommentViewSet(
        Votable,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin
):
    model = models.Comment
    serializer_class = serializers.CommentSerializer
    permission_classes = [QuestionOwnerOrStaffOrSafeMethod]


class QuestionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    Votable,
):
    model = models.Question
    serializer_class = serializers.QuestionSerializer
    permission_classes = [QuestionOwnerOrSafeMethodOrLoggedInCreate]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.QuestionListSerializer
        return serializers.QuestionSerializer

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def answers(self, request, pk):
        question = get_object_or_404(self.model, pk=pk)

        user = request.user
        user_profile = Profile.objects.get(user=user)
        try:
            text = request.data["text"]
            show_username = request.data["show_username"]
        except KeyError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        answer = models.Answer.objects.create(
            text=text,
            show_username=show_username,
            votes=Votes.objects.create(),
            owner=user_profile,
            parent=question,
            is_accepted=False,
        )

        serializer = serializers.AnswerSerializer(answer)
        return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # only the 'title', text', 'tags' can be updated
        allowed_keys = ["title", "text", "tags"]
        keys_to_delete = list()

        for key in request.data.keys():
            if key not in allowed_keys:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            request.data.pop(key, None)

        return super(QuestionViewSet, self).update(request, partial=True)

    def create(self, request, *args, **kwargs):
        # only the 'title', 'text', 'tags' can be posted
        allowed_keys = ["title", "text", "tags"]
        keys_to_delete = list()

        for key in request.data.keys():
            if key not in allowed_keys:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            request.data.pop(key, None)

        user_profile = request.user.profile

        try:
            title = request.data["title"]
            text = request.data["text"]
            tags = request.data["tags"]
        except KeyError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        question = models.Question.objects.create(
            title=title,
            text=text,
            votes=Votes.objects.create(),
            show_username=True,
            owner=user_profile,
            tags=tags,
        )
        serializer = serializers.QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def comments(self, request, pk):
        question = get_object_or_404(self.model, pk=pk)
        user_profile = request.user.profile
        try:
            text = request.data['text']
            show_username = request.data['show_username']
        except KeyError:
            return HttpResponseBadRequest('Text and show_username field cannot be empty!')
        comment = models.Comment.objects.create(
            text=text,
            show_username=show_username,
            votes=Votes.objects.create(),
            parent_question=question,
            owner=user_profile
        )
        serializer = serializers.CommentSerializer(comment)
        return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
