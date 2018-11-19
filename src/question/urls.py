from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'answers', views.AnswerViewSet)
router.register(r'questions', views.QuestionViewSet)
urlpatterns = router.urls
