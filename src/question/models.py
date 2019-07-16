from django.db import models
from soft_delete_it.models import SoftDeleteModel
from taggit.managers import TaggableManager
from taggit.models import TagBase, ItemBase

from account.models import Profile
from common.models import AbstractComment


class QuestionTag(TagBase, SoftDeleteModel):
    pass


class TaggedQuestion(ItemBase, SoftDeleteModel):
    tag = models.ForeignKey(
        QuestionTag,
        related_name="%(app_label)s_%(class)s_items",
        on_delete=models.CASCADE,
    )
    content_object = models.ForeignKey("Question", on_delete=models.CASCADE)

    @classmethod
    def tags_for(cls, model, instance=None, **extra_filters):
        kwargs = extra_filters or {}
        if instance is not None:
            kwargs.update({"%s__content_object" % cls.tag_relname(): instance})
            return cls.tag_model().objects.filter(**kwargs)
        kwargs.update({"%s__content_object__isnull" % cls.tag_relname(): False})
        return cls.tag_model().objects.filter(**kwargs).distinct()


class Question(AbstractComment):
    title = models.CharField(max_length=255)
    tags = TaggableManager(through=TaggedQuestion)

    def __str__(self):
        return self.title


class Answer(AbstractComment):
    is_accepted = models.BooleanField()
    parent = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers", null=False
    )


class Comment(AbstractComment):
    parent_answer = models.ForeignKey(
        "question.Answer",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )
    parent_question = models.ForeignKey(
        "question.Question",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )

    @property
    def parent(self):
        return self.parent_answer or self.parent_question


# TODO: It may need a middle class: https://django-taggit.readthedocs.io/en/latest/custom_tagging.html#custom-tag
class Course(TagBase):
    teacher = models.ForeignKey(
        Profile, related_name="courses", on_delete=models.CASCADE
    )
