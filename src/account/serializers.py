from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework import exceptions

from . import models


class OwnProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ("id", "full_name")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
        extra_kwargs = {"username": {"validators": [UnicodeUsernameValidator()]}}


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = models.Profile
        # fields = '__all__'
        exclude = ("avatar",)

    def create(self, validated_data):

        user_data = validated_data.pop("user")
        username = user_data.pop("username")

        user = User.objects.get(username=username)
        profile = models.Profile.objects.create(user=user, **validated_data)

        return profile

    def update(self, instance, validated_data):

        user_data = validated_data.pop("user")
        username = user_data.pop("username")
        user = User.objects.get(username=username)

        # update user
        user.email = user_data.pop("email")
        user.first_name = user_data.pop("first_name")
        user.last_name = user_data.pop("last_name")
        user.is_staff = user_data.pop("is_staff")
        user.is_active = user_data.pop("is_active")

        user.save()

        # update profile
        instance.user = user
        instance.about_me = validated_data["about_me"]
        instance.is_score_visible = validated_data["is_score_visible"]
        instance.ranked = validated_data["ranked"]

        instance.save()

        return instance


class ProfileSerializerBasicAccount(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = models.Profile
        exclude = ("avatar",)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        username = user_data.pop("username")

        user = User.objects.get(username=username)
        profile = models.Profile.objects.create(user=user, **validated_data)

        return profile

    def update(self, instance, validated_data):

        user_data = validated_data.pop("user")
        username = user_data.pop("username")
        user = User.objects.get(username=username)

        # update user
        user.email = user_data.pop("email")
        user.first_name = user_data.pop("first_name")
        user.last_name = user_data.pop("last_name")

        if user_data.pop("is_staff") != user.is_staff or user_data.pop("is_active") != user.is_active:
            raise exceptions.PermissionDenied

        user.save()

        # update profile
        instance.user = user
        instance.about_me = validated_data["about_me"]
        instance.is_score_visible = validated_data["is_score_visible"]
        instance.ranked = validated_data["ranked"]

        instance.save()

        return instance


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ("avatar",)
