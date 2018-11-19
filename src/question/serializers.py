from rest_framework import serializers
from common.serializers import AbstractCommentSerializer

from . import models
from account.models import Profile

class CommentSerializer(AbstractCommentSerializer):
    class Meta:
        model = models.Comment
        fields = (
            'text',
            'owner',
            'show_username',
            'vote_count',
            'user_vote'
        )
        read_only_fields = ('created_at', 'updated_at')

class AnswerSerializer(AbstractCommentSerializer):
    comments = CommentSerializer(many=True)

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

class QuestionSerializer(AbstractCommentSerializer):
    comments = CommentSerializer(many=True)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = models.Question
        fields = (
            'title',
            'text',
            'owner',
            'show_username',
            'vote_count',
            'user_vote',
            'comments',
            'answers'
        )
        read_only_fields = ('created_at', 'updated_at')
