from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    StudentViewSet,
    GroupViewSet,
    TestViewSet,
    TestScoreViewSet,
    save_chat_id,
)

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="student")
router.register(r"groups", GroupViewSet, basename="group")
router.register(r"tests", TestViewSet, basename="test")
router.register(r"scores", TestScoreViewSet, basename="score")

urlpatterns = [
    path("", include(router.urls)),
    path("save_chat_id/", save_chat_id, name="save_chat_id"),
]
