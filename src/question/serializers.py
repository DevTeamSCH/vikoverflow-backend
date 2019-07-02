from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer


from common.serializers import AbstractCommentSerializer
from . import models


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
            "id",
            "text",
            "owner",
            "vote_count",
            "user_vote",
            "is_accepted",
            "comments",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
            "owner",
            "vote_count",
            "user_vote",
            "is_accepted",
            "comments",
        )


class QuestionSerializer(TaggitSerializer, AbstractCommentSerializer):
    comments = CommentSerializer(many=True)
    answers = AnswerSerializer(many=True)
    tags = TagListSerializerField()

    class Meta:
        model = models.Question
        fields = (
            "id",
            "title",
            "text",
            "tags",
            "owner",
            "vote_count",
            "user_vote",
            "comments",
            "answers",
        )
        read_only_fields = ("created_at", "updated_at")


class QuestionListSerializer(TaggitSerializer, AbstractCommentSerializer):
    answer_count = serializers.SerializerMethodField()
    answered = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
        fields = (
            "id",
            "title",
            "owner",
            "vote_count",
            "user_vote",
            "answer_count",
            "answered",
        )
        read_only_fields = ("created_at", "updated_at")

    def get_answer_count(self, obj):
        return models.Answer.objects.filter(parent=obj.id).count()

    def get_answered(self, obj):
        return models.Answer.objects.filter(parent=obj.id, is_accepted=True).count()
