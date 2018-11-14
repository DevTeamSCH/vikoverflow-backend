from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg')
    about_me = models.TextField(blank=True)
    is_score_visible = models.BooleanField(default=False)
    ranked = models.BooleanField(default=False)

    @property
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        self.full_name
