from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from taggit.models import Tag

from . import models
from . import serializers
from account.models import Profile
from common.mixins import RelativeURLFieldMixin


class TagViewSet(
    RelativeURLFieldMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj, created = queryset.get_or_create(**filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
