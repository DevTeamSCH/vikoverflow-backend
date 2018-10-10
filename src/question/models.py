from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TagBase

from common.models import AbstractComment, Votes
from account.models import Profile


class Question(AbstractComment):
    title = models.CharField(max_length=255)
    tags = TaggableManager()
    parent = models.OneToOneField(Votes, related_name='question', on_delete=models.CASCADE, null=True)


class Answer(AbstractComment):
    is_accepted = models.BooleanField()
    parent = models.OneToOneField(Votes, related_name='answer', on_delete=models.CASCADE, null=True)


class Comment(AbstractComment):
    parent = models.OneToOneField(Votes, related_name='comment', on_delete=models.CASCADE, null=True)


# TODO: It may need a middle class: https://django-taggit.readthedocs.io/en/latest/custom_tagging.html#custom-tag
class Course(TagBase):
    teacher = models.ForeignKey(Profile, related_name='courses', on_delete=models.CASCADE)
