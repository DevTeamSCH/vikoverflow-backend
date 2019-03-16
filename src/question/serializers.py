from rest_framework import serializers
from common.serializers import AbstractCommentSerializer
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from . import models
from account.models import Profile


class CommentSerializer(AbstractCommentSerializer):
    # def validate(self, data):
    #     if data['parent_answer'] is None and data['parent_question'] is None:
    #         raise ValidationError(
    #             'Comment must have a parent answer or question!'
    #         )
    #     if data['parent_answer'] is not None and data['parent_question'] is not None:
    #         raise ValidationError(
    #             'Comment must only have one parent!'
    #         )
    #     return data

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'text',
            'show_username',
            'created_at',
            'updated_at',
            'username',
            'vote_count',
            'user_vote',
        )
        read_only_fields = ('created_at', 'updated_at', 'username', 'vote_count', 'user_vote',)
        

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
        read_only_fields = (
            'created_at', 'updated_at', 'owner', 'show_username', 'vote_count', 'user_vote', 'is_accepted', 'comments'
        )


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
