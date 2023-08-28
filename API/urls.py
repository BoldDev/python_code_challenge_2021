from rest_framework import routers
from django.urls import path, include
from .views import CommentsViewSet, EpisodesViewSet, SeasonsViewSet, TitlesViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register("titles", TitlesViewSet, basename="titles")
router.register("seasons", SeasonsViewSet, basename="seasons")
router.register("episodes", EpisodesViewSet, basename="episodes")
router.register("comments", CommentsViewSet, basename="comments")

urlpatterns = [path("", include(router.urls))]
