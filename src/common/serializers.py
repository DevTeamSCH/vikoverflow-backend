from rest_framework import serializers
from account.serializers import OwnProfileSerializer

from . import models


class AbstractCommentSerializer(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    owner = OwnProfileSerializer()

    class Meta:
        model = models.AbstractComment
        fields = ('text', 'owner', 'vote_count', 'user_vote')
        read_only_fields = ('created_at', 'updated_at')

    def get_vote_count(self, obj):
        upvotes = obj.votes.upvoters.count()
        downvotes = obj.votes.downvoters.count()
        return upvotes - downvotes

    def get_user_vote(self, obj):
        try:
            current = self.context['request'].user.username
            if obj.votes.upvoters.filter(
                    user__username=current
            ).count() > 0:
                return 'up'
            elif obj.votes.downvoters.filter(
                    user__username=current
            ).count() > 0:
                return 'down'
            else:
                return 'none'
        except KeyError:
            return 'none'
