from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TagBase

from common.models import AbstractComment
from account.models import Profile


class Question(AbstractComment):
    title = models.CharField(max_length=255)
    tags = TaggableManager()


class Answer(AbstractComment):
    is_accepted = models.BooleanField()


class Comment(AbstractComment):
    pass


# TODO: It may need a middle class: https://django-taggit.readthedocs.io/en/latest/custom_tagging.html#custom-tag
class Course(TagBase):
    teacher = models.ForeignKey(Profile, related_name='courses', on_delete=models.CASCADE)
