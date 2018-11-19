from rest_framework import serializers
from common.serializers import CommentSerializer

from . import models
from account.models import Profile

class AnswerSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    vote_count = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = models.Answer
        fields = (
            'text',
            'owner',
            'show_username',
            'vote_count',
            'user_vote',
            'is_accepted',
            'comments'
        )
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
                return False
        except:
            return False
