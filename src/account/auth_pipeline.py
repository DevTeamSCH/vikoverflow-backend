from django.core import exceptions
from django.shortcuts import redirect
from social_core.pipeline.partial import partial

from . import models


@partial
def create_profile(strategy, backend, request, details, user, *args, **kwargs):
    if backend.name == "authsch":
        try:
            user.profile
        except exceptions.ObjectDoesNotExist:
            display_name = strategy.session_get("displayName", None)
            if not display_name:
                return redirect("/first-login")
            models.Profile.objects.create(user=user, display_name=display_name)
