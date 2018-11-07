from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'accounts', views.ProfileViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = router.urls
