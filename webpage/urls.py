from django.urls import path
from . import views

app_name = "webpage"

urlpatterns = [
    path("home", views.home, name="home"),
    path(
        "seasons_and_episodes",
        views.season_and_episodes_view,
        name="seasons_and_episodes",
    ),
    path(
        "comments_web",
        views.comments_view,
        name="comments_web",
    ),
    path(
        "imdb_rating",
        views.episodes_imdb_rating,
        name="imdb_rating",
    ),
]
