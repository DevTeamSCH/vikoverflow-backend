from django.contrib.auth.models import User
from django.db import models

class ProfileManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(user__username=username)

class Profile(models.Model):
    objects = ProfileManager()
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
    about_me = models.TextField()
    is_score_visible = models.BooleanField(default=False)
    ranked = models.BooleanField(default=False)

    @property
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.full_name
