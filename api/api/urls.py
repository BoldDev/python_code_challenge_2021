from django.urls import path, include
from .views import CommentsViewSet, EpisodesViewSet, GenresViewSet, LanguagesViewSet, SeasonsViewSet, TitlesViewSet
from .views import FilterCommentsList, FilterEpisodesList, FilterSeasonsList, FilterTitlesList
from rest_framework import routers

router = routers.DefaultRouter()  # url manager
router.register("comments", CommentsViewSet, basename="comments")  # url registering on url manager
router.register("episodes", EpisodesViewSet, basename="episodes")
router.register("genres", GenresViewSet, basename="genres")
router.register("languages", LanguagesViewSet, basename="languages")
router.register("seasons", SeasonsViewSet, basename="seasons")
router.register("titles", TitlesViewSet, basename="titles")

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),  # adding all urls managed by url manager
    path("comments/<str:key>/<str:value>/", FilterCommentsList.as_view()),
    path("episodes/<str:key>/<str:value>/", FilterEpisodesList.as_view()),
    path("seasons/<str:key>/<str:value>/", FilterSeasonsList.as_view()),
    path("titles/<str:key>/<str:value>/", FilterTitlesList.as_view()),
]
