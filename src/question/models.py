from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TagBase

from common.models import Comment
from account.models import Profile


class Question(Comment):
    title = models.CharField(max_length=255)
    tags = TaggableManager()


class Answer(Comment):
    is_accepted = models.BooleanField()


# TODO: It may need a middle class: https://django-taggit.readthedocs.io/en/latest/custom_tagging.html#custom-tag
class Course(TagBase):
    teacher = models.ForeignKey(Profile, related_name='courses', on_delete=models.CASCADE)
