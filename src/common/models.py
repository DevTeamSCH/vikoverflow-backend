from django.db import models
from django.contrib.auth.models import User


class AbstractComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    show_username = models.BooleanField()
    text = models.TextField()
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    upvote = models.ManyToManyField(User, related_name='upvoted_comments')
    downvote = models.ManyToManyField(User, related_name='downvoted_comments')

    class Meta:
        abstract = True

    def __str__(self):
        return self.text
