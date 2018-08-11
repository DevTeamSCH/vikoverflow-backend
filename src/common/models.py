from django.db import models
from account.models import Profile


class AbstractComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    show_username = models.BooleanField()
    text = models.TextField()
    owner = models.ForeignKey(Profile, related_name='comments', on_delete=models.CASCADE)
    upvote = models.ManyToManyField(Profile, related_name='upvoted_comments')
    downvote = models.ManyToManyField(Profile, related_name='downvoted_comments')

    class Meta:
        abstract = True

    def __str__(self):
        return self.text
