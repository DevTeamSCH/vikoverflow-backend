from django.core import exceptions

from . import models


def create_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'authsch':
        try:
            user.profile
        except exceptions.ObjectDoesNotExist:
            models.Profile.objects.create(user=user)
