from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('question.urls')),
    path('api/v1/', include('account.urls')),
    path('api/v1/', include('social_django.urls', namespace='social')),
    path('api/v1/', include('moderate.urls')),
    path('api/v1/', include('feedback.urls')),
]
