from django.contrib.auth.models import User
from django.db import models
from soft_delete_it.models import SoftDeleteModel


class Profile(SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg')
    about_me = models.TextField(blank=True)
    is_score_visible = models.BooleanField(default=False)
    ranked = models.BooleanField(default=False)

    @property
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.full_name

    def delete(self, using=None):
        self.user.is_active = False
        self.user.save()
        super(Profile, self).delete(using)

    def undelete(self, using=None):
        self.user.is_active = True
        self.user.save()
        super(Profile, self).undelete(using)
