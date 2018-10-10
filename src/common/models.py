from django.db import models

from account.models import Profile


class AbstractComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    show_username = models.BooleanField()
    text = models.TextField()
    owner = models.ForeignKey(
        Profile,
        related_name="%(app_label)s_%(class)s_comments",
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Votes(models.Model):
        upvoters = models.ManyToManyField(
            Profile,
            related_name="upvotes",
        )
        downvoters = models.ManyToManyField(
            Profile,
            related_name="downvotes",
        )

        def __str__(self):
            return self.comment or self.answer or self.question
