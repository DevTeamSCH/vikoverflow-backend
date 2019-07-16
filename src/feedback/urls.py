from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r"tickets", views.TicketViewSet)
urlpatterns = router.urls
