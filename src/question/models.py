from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TagBase
from django.core.exceptions import ValidationError
from common.models import AbstractComment
from account.models import Profile


class Question(AbstractComment):
    title = models.CharField(max_length=255)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Answer(AbstractComment):
    is_accepted = models.BooleanField()
    parent = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        null=False
    )

class Comment(AbstractComment):
    parent_answer = models.ForeignKey(
        'question.Answer',
        on_delete=models.CASCADE,
        related_name='comments',
        null=True
    )
    parent_question = models.ForeignKey(
        'question.Question',
        on_delete=models.CASCADE,
        related_name='comments',
        null=True
    )

    @property
    def parent(self):
        return parent_answer or parent_question

    def clean(self):
        if parent_answer == None and parent_question == None:
            raise ValidationError(
                'Comment must have a parent answer or question!'
            )
        if parent_answer != None and parent_question != None:
            raise ValidationError(
                'Comment must only have one parent!'
            )


# TODO: It may need a middle class: https://django-taggit.readthedocs.io/en/latest/custom_tagging.html#custom-tag
class Course(TagBase):
    teacher = models.ForeignKey(Profile, related_name='courses', on_delete=models.CASCADE)
