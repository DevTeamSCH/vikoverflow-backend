from rest_framework import serializers

from . import models


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'
