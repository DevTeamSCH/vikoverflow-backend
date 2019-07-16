from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponseForbidden

from vikoverflow.settings import base


class DeployUserLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/v1/login") or request.path.startswith("/api/v1/complete") or base.ALLOWED_USERS == ['*']:
            return self.get_response(request)

        if not request.user.is_authenticated:
            return HttpResponseRedirect("/api/v1/login/authsch/")

        if request.user.username in base.ALLOWED_USERS:
            return self.get_response(request)

        logout(request)
        return HttpResponseForbidden()
