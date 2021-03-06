from django.contrib.auth import logout
from django.http import HttpResponseForbidden, HttpResponse

from vikoverflow.settings import base


class DeployUserLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            "/api/v1/login" in request.path
            or "/api/v1/complete" in request.path
            or base.ALLOWED_USERS == ["*"]
        ):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        if request.user.username in base.ALLOWED_USERS:
            return self.get_response(request)

        logout(request)
        return HttpResponseForbidden()
