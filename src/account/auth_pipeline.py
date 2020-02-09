from django.core import exceptions
from django.shortcuts import redirect
from social_core.pipeline.partial import partial
from rest_framework.response import Response

from . import models


@partial
def create_profile(strategy, backend, request, details, user, *args, **kwargs):
    if backend.name == "authsch":
        print(user)
        print(kwargs)
        try:
            user.profile
        except exceptions.ObjectDoesNotExist:
            display_name = strategy.session_get("displayName", None)
            if not display_name:
                print("Redirecting to /first-login ...")
                return redirect("/first-login")
            print(f"Creating profile with display name {display_name} ...")
            models.Profile.objects.create(user=user, display_name=display_name)
