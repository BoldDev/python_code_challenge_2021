from django.urls import path, re_path
from . import views

urlpatterns = [
    # Main page
    path('', views.index, name="series"),

    # 'Private' url to import data from OMDB
    path('fetch/', views.save_episodes, name="fetch"),

    # Fetch all seasons with all episodes
    path('seasons', views.get_seasons, name='seasons'),

    # Fetch a specific season with all episodes
    path('seasons/<int:season_id>', views.get_season_by_id, name='get_season_by_id'),

    # Fetch a specific season with a specific episode
    path('seasons/<int:season_id>/<int:episode_id>', views.get_season_by_id_by_episode, name='get_season_by_id_by_episode'),

    # COMMENTS TODO
    path('comments/<int:season_id>/<int:episode_id>', views.get_comments_by_id, name='get_comments_by_id'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]