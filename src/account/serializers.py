from django.contrib.auth.models import User
from rest_framework import serializers

from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'is_staff')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Profile
        #fields = ('url', 'user', 'avatar', 'about_me', 'is_score_visible', 'ranked')
        fields = '__all__'
