from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()]
            }
        }


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = models.Profile
        fields = '__all__'

    def create(self, validated_data):

        user_data = validated_data.pop('user')
        username = user_data.pop('username')

        user = User.objects.get(username=username)
        # ?  user = User.objects.get_or_create(username=username)[0]

        profile = models.Profile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user')
        username = user_data.pop('username')
        user = User.objects.get(username=username)
        # ? user = User.objects.get_or_create(username=username)[0]

        # update user
        user.email = user_data.pop('email')
        user.first_name = user_data.pop('first_name')
        user.last_name = user_data.pop('last_name')
        user.is_staff = user_data.pop('is_staff')
        user.is_active = user_data.pop('is_active')

        user.save()

        # update profile
        instance.user = user
        instance.avatar = validated_data['avatar']
        instance.about_me = validated_data['about_me']
        instance.is_score_visible = validated_data['is_score_visible']
        instance.ranked = validated_data['ranked']

        instance.save()

        return instance
