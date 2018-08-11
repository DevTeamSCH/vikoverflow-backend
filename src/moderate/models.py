from django.db import models
from django.contrib.auth.models import User


class ModeratorComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    owner = models.ForeignKey(User, related_name='moderate_comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text
