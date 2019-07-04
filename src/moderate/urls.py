from rest_framework.routers import DefaultRouter

from moderate.views import ReportViewSet

router = DefaultRouter()
router.register("reports", ReportViewSet)
urlpatterns = router.urls
