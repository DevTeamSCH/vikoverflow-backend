from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"accounts", views.ProfileViewSet)
router.register(r"avatar", views.AvatarViewSet)

urlpatterns = router.urls + [
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("display-name/", views.set_display_name),
]
