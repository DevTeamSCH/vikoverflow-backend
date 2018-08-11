from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
    about_me = models.TextField()
    is_score_visible = models.BooleanField()
    ranked = models.BooleanField()
