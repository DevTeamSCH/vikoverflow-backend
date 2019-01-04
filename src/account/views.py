from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions


from common.mixins import RelativeURLFieldMixin
from . permissions import CustomPerm
from . import models
from . import serializers


class ProfileViewSet(
    RelativeURLFieldMixin,
    generics.ListAPIView,
    generics.RetrieveUpdateAPIView,
    viewsets.GenericViewSet
):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, CustomPerm]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return serializers.ProfileSerializer
        return serializers.ProfileSerializerBasicAccount

    def get_queryset(self):

        queryset = models.Profile.objects.all()

        query_params = self.request.query_params

        if 'is_staff' in query_params:
            is_staff = query_params.get('is_staff')
            queryset = queryset.filter(user__is_staff=is_staff)

        elif 'username' in query_params:
            username = query_params.get('username')
            queryset = queryset.filter(user__username=username)

        elif 'is_active' in query_params:
            is_active = query_params.get('is_active')
            queryset = queryset.filter(user__is_active=is_active)

        return queryset


class AvatarViewSet(
    RelativeURLFieldMixin,
    generics.RetrieveUpdateAPIView,
    viewsets.GenericViewSet
):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.AvatarSerializer
    permission_classes = [permissions.IsAuthenticated, CustomPerm]
