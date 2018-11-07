from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics


from common.mixins import RelativeURLFieldMixin
from . import models
from . import serializers


class ProfileViewSet(
    #RelativeURLFieldMixin,
    generics.ListAPIView,
    generics.UpdateAPIView,
    generics.RetrieveAPIView,
    viewsets.GenericViewSet
):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        queryset = models.Profile.objects.all()

        #is_staff = self.request.query_params.get('is_staff')

        query_params = self.request.query_params

        if 'is_staff' in query_params:
            is_staff = query_params.get('is_staff')
            queryset = queryset.filter(user__is_staff=is_staff)

        elif 'username' in query_params:
            username = query_params.get('username')
            queryset = queryset.filter(user__username=username)

        return queryset


class UserViewSet(
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
    viewsets.GenericViewSet
):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
