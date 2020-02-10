from django.core import exceptions
from django.shortcuts import redirect
from social_core.pipeline.partial import partial

from . import models


@partial
def set_display_name(strategy, backend, is_new=False, *args, **kwargs):
    if not backend.name == "authsch" and not is_new:
        return
    display_name = strategy.session_get("displayName", None)
    if not display_name:
        return redirect("/first-login")


def create_profile(strategy, backend, request, details, user, *args, **kwargs):
    if not backend.name == "authsch":
        return
    try:
        user.profile
    except exceptions.ObjectDoesNotExist:
        display_name = strategy.session_get("displayName", None)
        models.Profile.objects.create(user=user, display_name=display_name)

