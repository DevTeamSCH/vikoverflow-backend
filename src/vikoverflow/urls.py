from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Vikoverflow API",
        default_version='v1',
        description="A vikoverflow API-ja",
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)


urlpatterns = [
    path("api/v1/", include("question.urls")),
    path("api/v1/", include("account.urls")),
    path("api/v1/", include("moderate.urls")),
    path("api/v1/", include("feedback.urls")),
    path("api/v1/", include("social_django.urls", namespace="social")),
    # Server Side Rendering
    path("admin/", admin.site.urls),
    url(r'^api/docs/swagger(?P<format>\.json|\.yaml)/$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
