from django.db import models

from account.models import Profile


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
            return ''.join([str(self.comment_item), '\'s votes'])


class AbstractComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    show_username = models.BooleanField()
    text = models.TextField()
    votes = models.OneToOneField(
        Votes,
        related_name='%(class)s_comment_item',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        Profile,
        related_name="%(app_label)s_%(class)s_comments",
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.text
