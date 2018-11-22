from rest_framework import serializers
from common.serializers import AbstractCommentSerializer
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

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


class QuestionSerializer(TaggitSerializer, AbstractCommentSerializer):
    comments = CommentSerializer(many=True)
    answers = AnswerSerializer(many=True)
    tags = TagListSerializerField()

    class Meta:
        model = models.Question
        fields = (
            'title',
            'text',
            'tags',
            'owner',
            'show_username',
            'vote_count',
            'user_vote',
            'comments',
            'answers'
        )
        read_only_fields = ('created_at', 'updated_at')
