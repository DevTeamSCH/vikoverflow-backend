from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'answers', views.AnswerViewSet, basename='answers')
router.register(r'comments', views.CommentViewSet, basename='comments')
router.register(r'questions', views.QuestionViewSet, basename='questions')
router.register(r'tags', views.TagViewSet)

urlpatterns = router.urls

