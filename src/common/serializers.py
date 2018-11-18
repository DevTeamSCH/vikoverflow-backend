from rest_framework import serializers

from . import models
from account.models import Profile

class CommentSerializer(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ('text', 'owner', 'show_username', 'vote_count', 'user_vote')
        read_only_fields = ('created_at', 'updated_at')

    def get_vote_count(self, obj):
        upvotes = obj.votes.upvoters.count()
        downvotes = obj.votes.downvoters.count()
        return upvotes - downvotes

    def get_user_vote(self, obj):
        try:
            current = Profile.objects.get(
                user__username=self.context['request'].user.username
            )
            if current in obj.votes.upvoters.all():
                return 'up'
            elif current in obj.votes.downvoters.all():
                return 'down'
            else:
                return False
        except:
            return False
